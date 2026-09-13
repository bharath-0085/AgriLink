"""
Agri Link — Buyer Models
=========================
"""

from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class BuyerProfile(BaseModel):
    """
    Buyer profile storing buyer-specific parameters.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="buyer_profile",
    )
    company_name = models.CharField(max_length=200, blank=True, default="")
    business_type = models.CharField(max_length=100, blank=True, default="")
    interest_categories = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "buyers"

    def __str__(self):
        return f"Buyer Profile: {self.user.name or self.user.username}"
