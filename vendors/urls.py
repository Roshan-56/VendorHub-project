from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
]