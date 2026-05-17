from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="Created")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.user.username