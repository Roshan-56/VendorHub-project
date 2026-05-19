# cart/urls.py
# Replace your entire cart/urls.py with this code.

from django.urls import path
from . import views

urlpatterns = [
    # View cart
    path('', views.cart_detail, name='cart_detail'),

    # Add product to cart
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Remove item from cart
    # IMPORTANT: uses remove_from_cart, not remove_item
    path('remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
]