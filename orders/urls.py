from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('track/<int:order_id>/', views.order_tracking, name='order_tracking'),
    path('vendor/', views.vendor_orders, name='vendor_orders'),
    path('update/<int:item_id>/', views.update_order_status, name='update_order_status'),
]