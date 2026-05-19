from django.shortcuts import render
from products.models import Product


def home(request):
    # Show latest 8 products on homepage
    products = Product.objects.all()[:8]

    return render(request, "home.html", {
        "products": products
    })