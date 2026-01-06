# services/admin.py
from django.contrib import admin
from .models import RepairShop, TowingProvider

@admin.register(RepairShop)
class RepairShopAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_vehicle_types', 'location', 'created_at']
    list_filter = ['vehicle_types']
    search_fields = ['user__username', 'user__email', 'amenities']
    readonly_fields = ['created_at', 'updated_at']

    def get_vehicle_types(self, obj):
        return ", ".join(obj.vehicle_types) if obj.vehicle_types else "None"
    get_vehicle_types.short_description = 'Vehicle Types'


@admin.register(TowingProvider)
class TowingProviderAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_vehicle_types', 'location', 'response_time', 'created_at']
    list_filter = ['vehicle_types']
    search_fields = ['user__username', 'user__email', 'amenities']
    readonly_fields = ['created_at', 'updated_at']

    def get_vehicle_types(self, obj):
        return ", ".join(obj.vehicle_types) if obj.vehicle_types else "None"
    get_vehicle_types.short_description = 'Vehicle Types'