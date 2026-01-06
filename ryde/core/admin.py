# core/admin.py
from django.contrib import admin
from .models import Vehicle, Location

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['owner', 'vehicle_type', 'name', 'model', 'vehicle_number', 'created_at']
    list_filter = ['vehicle_type', 'created_at']
    search_fields = ['vehicle_number', 'name', 'model', 'owner__username', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'created_at']
    search_fields = ['name', 'address']
    list_filter = ['created_at']
