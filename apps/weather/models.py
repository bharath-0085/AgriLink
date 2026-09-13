"""
Agri Link — Weather Cache Model
================================
Cache weather details by location (rounded lat/lng) to respect API rate limits.
"""

from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel


class WeatherCache(BaseModel):
    """
    Store weather API response data for a rounded GPS coordinate.
    """

    # We round GPS coordinates to 2 decimal places (approx. 1.1 km accuracy)
    # to group nearby requests and reuse cached data.
    lat = models.FloatField()
    lng = models.FloatField()
    data = models.JSONField(
        help_text="Raw response payload from OpenWeather API."
    )
    fetched_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "weather_cache"
        unique_together = ("lat", "lng")

    def __str__(self):
        return f"Weather Cache for ({self.lat}, {self.lng}) at {self.fetched_at}"

    def is_expired(self, ttl_seconds=1800):
        """Check if cached weather data has expired."""
        expiry = self.fetched_at + timedelta(seconds=ttl_seconds)
        return timezone.now() > expiry
