from django.db import models
from django.conf import settings


class VendorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    store_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name