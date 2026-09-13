"""
Agri Link — Marketplace Models
===============================
"""

from django.conf import settings
from django.db import models

from apps.core.constants import OrderStatus, QuantityUnit
from apps.core.models import BaseModel
from apps.core.validators import validate_latitude, validate_longitude, validate_positive_price


class Product(BaseModel):
    """
    Crops listed for sale by farmers.
    """

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listed_products",
    )
    crop_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(
        max_length=20,
        choices=QuantityUnit.CHOICES,
        default=QuantityUnit.KG,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_positive_price],
    )
    harvest_date = models.DateField()
    location = models.CharField(max_length=255, blank=True, default="")
    gps_lat = models.FloatField(
        null=True, blank=True, validators=[validate_latitude]
    )
    gps_lng = models.FloatField(
        null=True, blank=True, validators=[validate_longitude]
    )
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = "marketplace"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.crop_name} — {self.quantity} {self.unit}"


class ProductImage(BaseModel):
    """
    Images uploaded for a crop product listing.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image_url = models.URLField(max_length=500)

    class Meta:
        db_table = "marketplace_product_images"


class Order(BaseModel):
    """
    Order records for crop purchases by buyers.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_positive_price],
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.CHOICES,
        default=OrderStatus.PENDING,
    )

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} for {self.product.crop_name} by {self.buyer.name or self.buyer.username}"


class Bookmark(BaseModel):
    """
    Bookmarks/favorites of products by buyers.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="bookmarked_by",
    )

    class Meta:
        db_table = "bookmarks"
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} bookmarked {self.product.crop_name}"
