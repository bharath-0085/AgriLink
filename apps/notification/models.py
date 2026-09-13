"""
Agri Link — Notification Model
===============================
"""

from django.conf import settings
from django.db import models

from apps.core.constants import NotificationType
from apps.core.models import BaseModel


class Notification(BaseModel):
    """
    Stores system notifications sent to users.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.CHOICES,
        default=NotificationType.GENERAL,
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom key-value pairs associated with the notification.",
    )

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} for {self.user.username} (Read: {self.is_read})"
