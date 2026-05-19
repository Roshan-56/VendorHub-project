from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from vendorhub.views import home

urlpatterns = [
    # Home Page
    path('', home, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('vendors/', include('vendors.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)