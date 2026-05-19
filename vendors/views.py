from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def vendor_dashboard(request):
    return render(request, 'vendors/dashboard.html')