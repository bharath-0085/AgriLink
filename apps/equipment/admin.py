"""
Agri Link — Equipment Admin Configuration
=========================================
Registers Equipment and EquipmentBooking models with Django's administrative portal.
"""

from django.contrib import admin
from apps.equipment.models import Equipment, EquipmentBooking, EquipmentImage


class EquipmentImageInline(admin.TabularInline):
    model = EquipmentImage
    extra = 1


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """Admin configuration for Farm Machinery & Equipment Inventory."""
    list_display = (
        "name",
        "category",
        "owner",
        "daily_rent",
        "hourly_rent",
        "is_available",
        "location",
        "created_at",
    )
    list_filter = ("category", "is_available")
    search_fields = ("name", "owner__username", "owner__name", "location")
    ordering = ("-created_at",)
    inlines = [EquipmentImageInline]


@admin.register(EquipmentBooking)
class EquipmentBookingAdmin(admin.ModelAdmin):
    """Admin configuration for Machinery Rental Bookings."""
    list_display = (
        "id",
        "equipment",
        "renter",
        "start_date",
        "end_date",
        "total_cost",
        "status",
    )
    list_filter = ("status",)
    search_fields = ("equipment__name", "renter__username", "renter__name")
    ordering = ("-created_at",)
