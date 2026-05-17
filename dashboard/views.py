from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

from orders.models import OrderItem, Order
from vendors.models import VendorProfile


def vendor_dashboard(request):
    vendor = VendorProfile.objects.get(user=request.user)

    order_items = OrderItem.objects.filter(vendor=vendor)

    # Basic stats
    total_products = vendor.product_set.count()
    total_orders = order_items.values('order').distinct().count()

    revenue = sum([item.total_price for item in order_items])

    # -----------------------------
    # MONTHLY ANALYTICS (LAST 6 MONTHS)
    # -----------------------------
    labels = []
    data = []

    for i in range(5, -1, -1):
        month_date = now() - timedelta(days=30*i)
        month_items = order_items.filter(order__created_at__month=month_date.month)

        month_revenue = sum([item.total_price for item in month_items])

        labels.append(month_date.strftime("%b"))
        data.append(float(month_revenue))

    # -----------------------------
    # ORDER STATUS ANALYTICS
    # -----------------------------
    pending = Order.objects.filter(orderitem__vendor=vendor, status="Pending").distinct().count()
    shipped = Order.objects.filter(orderitem__vendor=vendor, status="Shipped").distinct().count()
    delivered = Order.objects.filter(orderitem__vendor=vendor, status="Delivered").distinct().count()

    return render(request, 'dashboard/vendor_dashboard.html', {
        'vendor': vendor,
        'total_products': total_products,
        'total_orders': total_orders,
        'revenue': revenue,

        # charts
        'labels': labels,
        'data': data,

        # order stats
        'pending': pending,
        'shipped': shipped,
        'delivered': delivered,
    })
from django.shortcuts import render
from orders.models import OrderItem
from django.conf import settings


def admin_commission_dashboard(request):

    items = OrderItem.objects.all()

    total_sales = 0
    total_commission = 0
    total_vendor_earnings = 0

    for item in items:
        item_total = item.price * item.quantity

        total_sales += item_total
        total_commission += item.commission_amount()
        total_vendor_earnings += item.vendor_earnings()

    return render(request, "dashboard/commission_dashboard.html", {
        "total_sales": total_sales,
        "total_commission": total_commission,
        "total_vendor_earnings": total_vendor_earnings,
        "commission_rate": settings.PLATFORM_COMMISSION_RATE
    })