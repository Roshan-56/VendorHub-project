from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('tracking/<int:order_id>/', views.order_tracking, name='order_tracking'),

    # Dashboards
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('commission/', views.commission_dashboard, name='commission_dashboard'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
]