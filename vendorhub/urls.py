from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),  # 👈 HOME PAGE
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('vendors/', include('vendors.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('dashboard/', include('dashboard.urls')),
]