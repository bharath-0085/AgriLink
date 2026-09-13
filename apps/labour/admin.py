"""
Agri Link — Labour Admin Configuration
======================================
Registers Job and LabourProfile models with Django's administrative portal.
"""

from django.contrib import admin
from apps.labour.models import Job, LabourProfile


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Admin configuration for Labour Job Postings."""
    list_display = (
        "title",
        "farmer",
        "labour",
        "wage",
        "wage_type",
        "status",
        "location",
        "created_at",
    )
    list_filter = ("status", "wage_type")
    search_fields = ("title", "farmer__username", "farmer__name", "location")
    ordering = ("-created_at",)


@admin.register(LabourProfile)
class LabourProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Labour Worker Profiles."""
    list_display = (
        "user",
        "experience_years",
        "daily_wage",
        "is_available",
    )
    list_filter = ("is_available",)
    search_fields = ("user__username", "user__name")
