# core/models.py
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser

# Vehicle Type Choices
VEHICLE_TYPE_CHOICES = (
    ('car', 'Car'),
    ('bike', 'Bike'),
    ('other', 'Other Vehicle'),
)

# Breakdown / Issue Choices
CAR_ISSUES = [
    ('engine_failure', 'Engine Failure'),
    ('battery_dead', 'Battery Dead'),
    ('fuel_leakage', 'Fuel Leakage / Fuel Issue'),
    ('overheating', 'Overheating'),
    ('electrical_fault', 'Electrical Fault'),
    ('brake_failure', 'Brake Failure'),
    ('alternator_failure', 'Alternator Failure'),
    ('radiator_leak', 'Radiator Leak'),
    ('transmission_failure', 'Transmission Failure'),
    ('power_steering_failure', 'Power Steering Failure'),
    ('starter_motor_issue', 'Starter Motor Issue'),
    ('ac_compressor_failure', 'AC Compressor Failure'),
]

BIKE_ISSUES = [
    ('engine_failure', 'Engine Failure'),
    ('battery_dead', 'Battery Dead'),
    ('fuel_leakage', 'Fuel Leakage / Fuel Issue'),
    ('overheating', 'Overheating'),
    ('electrical_fault', 'Electrical Fault'),
    ('brake_failure', 'Brake Failure'),
    ('chain_break', 'Chain Break / Chain Jam'),
    ('clutch_cable_break', 'Clutch Cable Break'),
    ('kick_start_failure', 'Kick Start Failure'),
    ('carburetor_blockage', 'Carburetor Blockage'),
    ('spark_plug_failure', 'Spark Plug Failure'),
    ('gear_shifter_issue', 'Gear Shifter Issue'),
]

OTHER_VEHICLE_ISSUES = [
    ('engine_failure', 'Engine Failure'),
    ('battery_dead', 'Battery Dead'),
    ('fuel_leakage', 'Fuel Leakage / Fuel Issue'),
    ('overheating', 'Overheating'),
    ('electrical_fault', 'Electrical Fault'),
    ('brake_failure', 'Brake Failure'),
    ('air_brake_failure', 'Air Brake Failure'),
    ('axle_break', 'Axle Break'),
    ('differential_failure', 'Differential Failure'),
    ('suspension_failure', 'Suspension Failure'),
    ('turbocharger_failure', 'Turbocharger Failure'),
    ('hydraulic_system_failure', 'Hydraulic System Failure'),
]

class Vehicle(models.Model):
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'owner'},
        related_name='vehicles'
    )
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
    name = models.CharField(max_length=100, help_text="e.g., Honda Civic, Yamaha R15")
    model = models.CharField(max_length=100, blank=True)
    vehicle_number = models.CharField(max_length=20, unique=True, help_text="License plate number")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.vehicle_number}) - {self.get_vehicle_type_display()}"

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        ordering = ['-created_at']


class Location(models.Model):
    """
    Reusable location model with geospatial PointField.
    Used by: Repair Shops, Towing Providers, and temporary user location during booking.
    """
    name = models.CharField(max_length=200, blank=True, help_text="e.g., Shop Name or 'User Current Location'")
    point = gis_models.PointField(default=Point(0.0, 0.0), geography=True)  # Longitude, Latitude
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Location ({self.point.coords[1]:.4f}, {self.point.coords[0]:.4f})"

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'