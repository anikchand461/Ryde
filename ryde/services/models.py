# services/models.py
from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from core.models import (
    Location, VEHICLE_TYPE_CHOICES,
    CAR_ISSUES, BIKE_ISSUES, OTHER_VEHICLE_ISSUES
)

class ServiceProviderBase(models.Model):
    """
    Abstract base for shared fields between RepairShop and TowingProvider.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='%(class)s_profile'
    )
    vehicle_types = models.JSONField(
        default=list,
        blank=True,
        help_text="List of vehicle types handled, e.g., ['car', 'bike']"
    )
    location = models.OneToOneField(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_location'
    )
    timings = models.JSONField(
        default=dict,
        blank=True,
        help_text="e.g., {'monday': '9am-5pm', 'tuesday': '9am-5pm', ...}"
    )
    amenities = models.TextField(
        blank=True,
        help_text="Comma-separated list or description of amenities (e.g., WiFi, Waiting Area)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} - {self.user.get_user_type_display()}"        

class RepairShop(ServiceProviderBase):
    """
    Model for Repair Shops/Mechanics.
    """
    car_issues = models.JSONField(
        default=list,
        blank=True,
        help_text="List of car issues handled, e.g., ['engine_failure', 'battery_dead']"
    )
    bike_issues = models.JSONField(
        default=list,
        blank=True,
        help_text="List of bike issues handled"
    )
    other_issues = models.JSONField(
        default=list,
        blank=True,
        help_text="List of other vehicle issues handled"
    )

    class Meta:
        verbose_name = 'Repair Shop'
        verbose_name_plural = 'Repair Shops'


class TowingProvider(ServiceProviderBase):
    """
    Model for Towing Services.
    """
    towing_types = models.TextField(
        blank=True,
        help_text="e.g., Flatbed Towing, Wheel-Lift Towing, Heavy-Duty Towing"
    )
    response_time = models.CharField(
        max_length=50,
        blank=True,
        help_text="Average response time (e.g., 30 minutes)"
    )

    class Meta:
        verbose_name = 'Towing Provider'
        verbose_name_plural = 'Towing Providers'
