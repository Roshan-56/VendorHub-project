from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse

import razorpay

from cart.models import Cart, CartItem
from .models import Order, OrderItem
from vendors.models import VendorProfile
from products.models import Product

from .utils import (
    send_order_confirmation_email,
    send_vendor_new_order_email,
    send_payment_success_email
)

# Razorpay client
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


# ---------------------------
# CHECKOUT (CREATE ORDER)
# ---------------------------
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('product_list')

    total = sum(item.product.price * item.quantity for item in cart_items)

    # Create Razorpay Order
    razorpay_order = client.order.create({
        "amount": int(total * 100),  # paise
        "currency": "INR",
        "payment_capture": 1
    })

    # Create Order in DB
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        payment_id=razorpay_order['id'],
        status="Pending"
    )

    # Create Order Items (MULTI VENDOR)
    for item in cart_items:
        product = item.product

        OrderItem.objects.create(
            order=order,
            product=product,
            vendor=product.vendor,
            quantity=item.quantity,
            price=product.price
        )

    # Clear cart
    cart_items.delete()

    # Send email (order placed)
    send_order_confirmation_email(order, request.user.email)

    return render(request, "orders/payment_page.html", {
        "order": order,
        "razorpay_order": razorpay_order,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


# ---------------------------
# PAYMENT SUCCESS HANDLER
# ---------------------------
@login_required
def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')

    order = get_object_or_404(Order, payment_id=order_id)

    order.status = "Processing"
    order.save()

    # Send success emails
    send_payment_success_email(order, request.user.email)

    # Vendor notifications
    vendors = set(
        item.vendor.user.email
        for item in order.orderitem_set.all()
        if item.vendor
    )

    for email in vendors:
        send_vendor_new_order_email(email, order)

    return render(request, "orders/payment_success.html", {
        "order": order
    })


# ---------------------------
# ORDER TRACKING (CUSTOMER)
# ---------------------------
@login_required
def order_tracking(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    items = OrderItem.objects.filter(order=order)

    return render(request, "orders/order_tracking.html", {
        "order": order,
        "items": items
    })


# ---------------------------
# VENDOR DASHBOARD ORDERS
# ---------------------------
@login_required
def vendor_orders(request):
    vendor = get_object_or_404(VendorProfile, user=request.user)

    items = OrderItem.objects.filter(vendor=vendor).order_by('-created_at')

    return render(request, "orders/vendor_orders.html", {
        "items": items
    })


# ---------------------------
# VENDOR UPDATE ORDER STATUS
# ---------------------------
@login_required
def update_order_status(request, item_id):
    vendor = get_object_or_404(VendorProfile, user=request.user)
    item = get_object_or_404(OrderItem, id=item_id, vendor=vendor)

    if request.method == "POST":
        item.status = request.POST.get("status")
        item.save()

    return redirect('vendor_orders')