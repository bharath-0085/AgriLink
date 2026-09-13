"""
Agri Link — Accounts Admin Configuration
========================================
Registers User model with Django's administrative portal.
"""

from django.contrib import admin
from apps.accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for custom User model."""
    list_display = (
        "username",
        "name",
        "phone",
        "role",
        "district",
        "is_verified",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = ("role", "is_verified", "is_active", "is_staff")
    search_fields = ("username", "name", "phone", "district", "email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
