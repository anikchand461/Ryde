# bookings/models.py
from django.db import models
from django.utils import timezone
from django.contrib.gis.db.models import PointField

from accounts.models import CustomUser
from core.models import Vehicle, Location, CAR_ISSUES, BIKE_ISSUES, OTHER_VEHICLE_ISSUES
from services.models import RepairShop, TowingProvider

class Booking(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('repair', 'Repair Service'),
        ('towing', 'Towing Service'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'owner'},
        related_name='bookings'
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES)
    
    # Provider (can be either RepairShop or TowingProvider)
    repair_shop = models.ForeignKey(
        RepairShop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repair_bookings'
    )
    towing_provider = models.ForeignKey(
        TowingProvider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='towing_bookings'
    )

    # Issue selected
    issue = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    # User location at time of booking
    user_location = PointField(geography=True, null=True, blank=True)
    user_address = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.service_type.title()} Booking - {self.vehicle} ({self.status})"

    def can_cancel(self):
        """Owner can cancel within 2 minutes"""
        if self.status != 'pending':
            return False
        time_diff = timezone.now() - self.created_at
        return time_diff.total_seconds() <= 120  # 2 minutes

    @property
    def provider(self):
        return self.repair_shop or self.towing_provider

    @property
    def provider_user(self):
        if self.repair_shop:
            return self.repair_shop.user
        elif self.towing_provider:
            return self.towing_provider.user
        return None