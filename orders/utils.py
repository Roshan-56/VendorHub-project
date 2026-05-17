from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order, user_email):
    subject = f"Order Confirmation - Order #{order.id}"

    message = f"""
    Thank you for your order!

    Order ID: {order.id}
    Total Amount: ₹{order.total_amount}

    Your order is being processed.
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )


def send_vendor_new_order_email(vendor_email, order):
    subject = f"New Order Received - Order #{order.id}"

    message = f"""
    You have received a new order!

    Order ID: {order.id}
    Please check your dashboard.
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [vendor_email],
        fail_silently=False
    )


def send_payment_success_email(order, user_email):
    subject = f"Payment Successful - Order #{order.id}"

    message = f"""
    Payment successful!

    Order ID: {order.id}
    Amount Paid: ₹{order.total_amount}

    Thank you for shopping with VendorHub.
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )