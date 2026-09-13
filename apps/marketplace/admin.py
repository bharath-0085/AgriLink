"""
Agri Link — Marketplace Admin Configuration
===========================================
Registers Product and Order models with Django's administrative portal.
"""

from django.contrib import admin
from apps.marketplace.models import Product, Order, Bookmark, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for farmer Crop Product listings."""
    list_display = (
        "crop_name",
        "farmer",
        "quantity",
        "unit",
        "price",
        "location",
        "is_available",
        "created_at",
    )
    list_filter = ("is_available", "unit")
    search_fields = ("crop_name", "farmer__username", "farmer__name", "location")
    ordering = ("-created_at",)
    inlines = [ProductImageInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Crop Marketplace Orders."""
    list_display = (
        "id",
        "product",
        "buyer",
        "quantity",
        "total_price",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("product__crop_name", "buyer__username", "buyer__name")
    ordering = ("-created_at",)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "created_at")
