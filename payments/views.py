# payments/views.py
# This version works even if Razorpay keys are not configured.
# It removes redirects to non-existent views like order_detail or order_history.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from orders.models import Order

# Optional Razorpay support
try:
    import razorpay

    if (
        hasattr(settings, "RAZORPAY_KEY_ID")
        and hasattr(settings, "RAZORPAY_KEY_SECRET")
        and settings.RAZORPAY_KEY_ID
        and settings.RAZORPAY_KEY_SECRET
    ):
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
    else:
        client = None
except ImportError:
    client = None


@login_required
def initiate_payment(request, order_id):
    """
    Opens the payment page.
    If Razorpay is configured, creates a Razorpay order.
    Otherwise, shows a demo payment page.
    """
    order = get_object_or_404(Order, id=order_id)

    # Optional ownership check
    if hasattr(order, "user") and order.user != request.user:
        messages.error(request, "You are not allowed to access this order.")
        return redirect("order_list")

    context = {
        "order": order,
        "razorpay_order_id": "",
        "razorpay_key_id": "",
        "amount": int(order.total_amount * 100),
        "currency": "INR",
        "razorpay_enabled": False,
    }

    # If Razorpay is available, create real Razorpay order
    if client:
        try:
            amount_in_paise = int(order.total_amount * 100)

            razorpay_order = client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1,
            })

            # Save payment ID if field exists
            if hasattr(order, "payment_id"):
                order.payment_id = razorpay_order["id"]
                order.save()

            context.update({
                "razorpay_order_id": razorpay_order["id"],
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "amount": amount_in_paise,
                "currency": "INR",
                "razorpay_enabled": True,
            })

        except Exception:
            # Fall back to demo mode if Razorpay fails
            messages.warning(
                request,
                "Razorpay is not configured correctly. Showing demo payment page."
            )

    return render(request, "payments/payment_page.html", context)


@login_required
def payment_success(request):
    """
    Marks the order as paid and redirects to order tracking.
    Works both with and without Razorpay verification.
    """
    order = None

    # 1. Try to find order using Razorpay order ID
    razorpay_order_id = request.POST.get("razorpay_order_id")
    if razorpay_order_id:
        try:
            order = Order.objects.get(payment_id=razorpay_order_id)
        except Exception:
            order = None

    # 2. Fallback: use explicit order_id
    if order is None:
        order_id = request.POST.get("order_id") or request.GET.get("order_id")
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
            except Exception:
                order = None

    # 3. If no order found
    if order is None:
        messages.error(request, "Order not found.")
        return redirect("order_list")

    # Optional ownership check
    if hasattr(order, "user") and order.user != request.user:
        messages.error(request, "You are not allowed to access this order.")
        return redirect("order_list")

    # Mark as paid
    if hasattr(order, "status"):
        order.status = "paid"
        order.save()

    messages.success(request, "Payment completed successfully!")

    # Redirect to tracking page
    return redirect("order_tracking", order_id=order.id)


@login_required
def payment_failed(request):
    """
    Called when payment fails or user cancels.
    """
    messages.error(request, "Payment failed or was cancelled.")
    return redirect("order_list")