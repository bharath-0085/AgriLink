"""
Agri Link — Core Models
========================
Base model and shared models (Review, Rating) used across the project.
"""

from django.db import models
from django.conf import settings
from apps.core.constants import ReviewType


class BaseModel(models.Model):
    """Abstract base model providing audit timestamps and soft-delete flag."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Review(BaseModel):
    """
    Cross-cutting review/rating model.
    Supports reviews for farmers, labourers, equipment, and products.
    """

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_given",
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_received",
        null=True,
        blank=True,
    )
    target_id = models.CharField(
        max_length=64,
        blank=True,
        default="",
        help_text="ID of reviewed entity (equipment, product) when reviewee is null.",
    )
    review_type = models.CharField(max_length=20, choices=ReviewType.CHOICES)
    rating = models.PositiveSmallIntegerField(
        help_text="Rating from 1 to 5.",
    )
    comment = models.TextField(blank=True, default="")

    class Meta:
        db_table = "reviews"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review by {self.reviewer_id} — {self.rating}/5"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.rating < 1 or self.rating > 5:
            raise ValidationError({"rating": "Rating must be between 1 and 5."})
