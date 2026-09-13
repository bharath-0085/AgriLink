"""
Agri Link — AI Module Models
==============================
"""

from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class CropPrediction(BaseModel):
    """
    Cache of AI crop recommendation results.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="crop_predictions",
        null=True,
        blank=True,
    )
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    recommended_crop = models.CharField(max_length=100)
    confidence = models.FloatField()

    class Meta:
        db_table = "crop_predictions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Crop Prediction: {self.recommended_crop} at {self.created_at}"


class DiseasePrediction(BaseModel):
    """
    Cache of AI plant disease recognition results.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="disease_predictions",
        null=True,
        blank=True,
    )
    image_url = models.URLField(max_length=500)
    predicted_disease = models.CharField(max_length=200)
    confidence = models.FloatField()

    class Meta:
        db_table = "disease_predictions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Disease Prediction: {self.predicted_disease} at {self.created_at}"


class ChatbotHistory(models.Model):
    """
    Stores per-user AI chatbot conversation history.
    Each record is one message turn (user or bot).
    """
    ROLE_USER = "user"
    ROLE_BOT = "bot"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_BOT, "Bot"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chatbot_history",
        null=True,
        blank=True,
    )
    session_id = models.CharField(
        max_length=64,
        blank=True,
        default="",
        help_text="Optional session identifier for grouping conversations.",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chatbot_history"
        ordering = ["timestamp"]

    def __str__(self):
        user_label = self.user.username if self.user else "Anonymous"
        return f"[{self.role}] {user_label}: {self.message[:50]}"
