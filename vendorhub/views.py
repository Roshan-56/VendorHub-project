from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>VendorHub Marketplace is Running 🚀</h1>")