# orders/views.py
# Replace your ENTIRE orders/views.py with this complete code.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.models import Cart
from .models import Order, OrderItem


# orders/views.py
# Replace ONLY the checkout() function with this corrected version.
# Your current Order model does NOT contain an 'address' field.

# orders/views.py
# Replace ONLY the checkout() function with this version.
# Your MySQL database still requires the 'address' column,
# so we must provide it when creating the Order.

@login_required
def checkout(request):
    """
    Create an order from the user's cart and redirect to payment.
    """

    # Get user's cart
    cart = Cart.objects.filter(user=request.user).first()

    # Check if cart is empty
    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    # Get cart items
    cart_items = cart.items.all()

    # Calculate total amount
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    # Create order
    # IMPORTANT: Even if your current Order model does not show 'address',
    # the database table still has this required column.
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status="pending",
        address="Default Delivery Address"
    )

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            vendor=getattr(item.product, "vendor", None)
        )

    # Clear cart after successful order creation
    cart.items.all().delete()

    messages.success(request, "Order created successfully.")

    # Redirect to payment page
    return redirect("initiate_payment", order_id=order.id)

@login_required
def order_list(request):
    """
    Show all orders for the logged-in user.
    """
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "orders/order_list.html", {
        "orders": orders
    })


@login_required
def order_tracking(request, order_id):
    """
    Show tracking information for a specific order.
    """
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(request, "orders/order_tracking.html", {
        "order": order
    })


@login_required
def vendor_dashboard(request):
    """
    Vendor dashboard page.
    """
    return render(request, "orders/vendor_dashboard.html")


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def commission_dashboard(request):
    return render(request, 'orders/commission_dashboard.html')


# orders/views.py
# Replace ONLY the analytics_dashboard() function with this code.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Order, OrderItem
from products.models import Product
from vendors.models import VendorProfile


@login_required
def analytics_dashboard(request):
    # Total Revenue (only paid orders)
    total_revenue = (
        Order.objects.filter(status='paid')
        .aggregate(total=Sum('total_amount'))['total'] or 0
    )

    # Total Orders
    total_orders = Order.objects.count()

    # Active Vendors
    active_vendors = VendorProfile.objects.count()

    # Total Products
    total_products = Product.objects.count()

    # Paid Orders
    paid_orders = Order.objects.filter(status='paid').count()

    # Pending Orders
    pending_orders = Order.objects.filter(status='pending').count()

    # Success Rate
    if total_orders > 0:
        success_rate = round((paid_orders / total_orders) * 100, 2)
    else:
        success_rate = 0

    # Top Selling Products
    top_products = (
        OrderItem.objects
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'active_vendors': active_vendors,
        'total_products': total_products,
        'paid_orders': paid_orders,
        'pending_orders': pending_orders,
        'success_rate': success_rate,
        'top_products': top_products,
    }

    return render(request, 'orders/analytics_dashboard.html', context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Order
from products.models import Product


@login_required
def vendor_dashboard(request):
    total_sales = (
        Order.objects.filter(status='paid')
        .aggregate(total=Sum('total_amount'))['total'] or 0
    )

    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    recent_orders = Order.objects.order_by('-id')[:5]

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_products': total_products,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
    }

    return render(request, 'orders/vendor_dashboard.html', context)