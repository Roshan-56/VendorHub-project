# payments/urls.py
# Replace your entire file with this code.

from django.urls import path
from django.http import HttpResponse
from . import views


def payment_home(request):
    """
    This fixes the 404 when visiting:
    http://127.0.0.1:8000/payments/
    """
    return HttpResponse("""
    <h1>Payment System</h1>
    <p>Select a payment action:</p>
    <ul>
        <li><a href="/payments/initiate/1/">Initiate Payment for Order #1</a></li>
        <li><a href="/payments/success/?order_id=1">Demo Payment Success</a></li>
    </ul>
    """)


urlpatterns = [
    # Fixes /payments/
    path('', payment_home, name='payment_home'),

    # Existing payment routes
    path('initiate/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]