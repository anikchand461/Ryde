# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('owner', 'Vehicle Owner/Driver'),
        ('repair_shop', 'Repair Shop/Mechanic'),
        ('towing', 'Towing Service Provider'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='owner'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username or self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'