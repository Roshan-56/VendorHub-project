from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        payment = Payment.objects.get(razorpay_order_id=order_id)

        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = "Paid"
        payment.save()

        # update order
        order = payment.order
        order.paid = True
        order.payment_id = payment_id
        order.status = "Processing"
        order.save()

        return redirect("order_success")

    return HttpResponse("Invalid Request")