"""
Agri Link — Equipment Models
=============================
"""

from django.conf import settings
from django.db import models

from apps.core.constants import EquipmentCategory, BookingStatus
from apps.core.models import BaseModel
from apps.core.validators import validate_latitude, validate_longitude, validate_positive_price


class Equipment(BaseModel):
    """
    Equipment listed for rent by equipment owners or farmers.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listed_equipment",
    )
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=EquipmentCategory.CHOICES,
        default=EquipmentCategory.OTHER,
    )
    purpose = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField()
    hourly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_positive_price],
    )
    daily_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_positive_price],
    )
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True, default="")
    gps_lat = models.FloatField(
        null=True, blank=True, validators=[validate_latitude]
    )
    gps_lng = models.FloatField(
        null=True, blank=True, validators=[validate_longitude]
    )

    class Meta:
        db_table = "equipment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class EquipmentImage(BaseModel):
    """
    Images uploaded for a specific equipment listing.
    """

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image_url = models.URLField(max_length=500)

    class Meta:
        db_table = "equipment_images"


class EquipmentBooking(BaseModel):
    """
    Booking record when a farmer rents an equipment.
    """

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="equipment_bookings",
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.CHOICES,
        default=BookingStatus.PENDING,
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_positive_price],
    )

    class Meta:
        db_table = "rentals"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Booking {self.id} for {self.equipment.name} by {self.renter.name or self.renter.username}"
