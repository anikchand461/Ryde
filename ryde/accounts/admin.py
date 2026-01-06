# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'whatsapp_number')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'whatsapp_number', 'email')
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'phone_number']
    list_filter = ['user_type'] + list(UserAdmin.list_filter)
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']