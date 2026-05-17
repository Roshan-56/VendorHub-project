from django.urls import path
from . import views

urlpatterns = [
    path('commission/', views.admin_commission_dashboard, name='commission_dashboard'),
]