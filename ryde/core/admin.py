# core/admin.py
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Vehicle, Location

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['owner', 'vehicle_type', 'name', 'model', 'vehicle_number']
    list_filter = ['vehicle_type']
    search_fields = ['vehicle_number', 'name', 'model', 'owner__username', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Location)
class LocationAdmin(OSMGeoAdmin):
    list_display = ['name', 'address_short', 'created_at']
    search_fields = ['name', 'address']

    def address_short(self, obj):
        return obj.address[:50] + "..." if len(obj.address) > 50 else obj.address
    address_short.short_description = 'Address'