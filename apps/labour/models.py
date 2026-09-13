"""
Agri Link — Labour Models
===========================
Labour profile and job models.
"""

from django.conf import settings
from django.db import models

from apps.core.constants import JobStatus
from apps.core.models import BaseModel
from apps.core.validators import validate_latitude, validate_longitude, validate_positive_price


class LabourProfile(BaseModel):
    """
    Extended profile for labourers.
    Contains skills, experience, wage, and availability info.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="labour_profile",
    )
    skills = models.JSONField(
        default=list,
        blank=True,
        help_text="List of skill strings, e.g. ['ploughing', 'harvesting']",
    )
    experience_years = models.PositiveIntegerField(default=0)
    daily_wage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[validate_positive_price],
    )
    is_available = models.BooleanField(default=True)
    bio = models.TextField(blank=True, default="")

    class Meta:
        db_table = "labours"

    def __str__(self):
        return f"Labour: {self.user.name or self.user.username}"


class Job(BaseModel):
    """
    Job posting by a farmer, to be accepted/rejected by labourers.
    """

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posted_jobs",
    )
    labour = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_jobs",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    wage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_positive_price],
    )
    wage_type = models.CharField(
        max_length=10,
        choices=[("daily", "Daily"), ("hourly", "Hourly"), ("fixed", "Fixed")],
        default="daily",
    )
    status = models.CharField(
        max_length=20,
        choices=JobStatus.CHOICES,
        default=JobStatus.OPEN,
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, default="")
    gps_lat = models.FloatField(
        null=True, blank=True, validators=[validate_latitude],
    )
    gps_lng = models.FloatField(
        null=True, blank=True, validators=[validate_longitude],
    )
    required_skills = models.JSONField(default=list, blank=True)
    num_workers = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "jobs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.status}"
