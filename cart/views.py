# cart/views.py
# Your Cart model does NOT have a direct 'product' field.
# It has a related model called CartItem through the reverse relation 'items'.
# Replace your entire cart/views.py with this code.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cart, CartItem
from products.models import Product


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the user's cart.
    Uses Cart and CartItem models.
    """
    product = get_object_or_404(Product, id=product_id)

    # Get or create cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create CartItem inside that cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": 1}
    )

    # If already exists, increase quantity
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect("cart_detail")


@login_required
def cart_detail(request):
    """
    Display all items in the user's cart.
    """
    # Get cart if it exists
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return render(request, "cart/cart_detail.html", {
            "cart_items": [],
            "total": 0,
        })

    # Related name is 'items'
    cart_items = cart.items.all()

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, "cart/cart_detail.html", {
        "cart_items": cart_items,
        "total": total,
    })


@login_required
def remove_from_cart(request, cart_id):
    """
    Remove a CartItem by its ID.
    URL passes cart_id, but this is actually the CartItem ID.
    """
    cart = get_object_or_404(Cart, user=request.user)

    cart_item = get_object_or_404(
        CartItem,
        id=cart_id,
        cart=cart
    )

    cart_item.delete()

    messages.success(request, "Item removed from cart.")
    return redirect("cart_detail")