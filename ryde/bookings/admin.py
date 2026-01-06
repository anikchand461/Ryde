# bookings/admin.py
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'vehicle', 'service_type', 'status', 'created_at']
    list_filter = ['service_type', 'status', 'created_at']
    search_fields = ['owner__username', 'vehicle__vehicle_number', 'issue']
    readonly_fields = ['created_at', 'updated_at', 'accepted_at']
