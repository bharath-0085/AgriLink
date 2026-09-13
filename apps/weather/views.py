"""
Agri Link — Weather Views
===========================
"""

import logging
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from apps.core.utils import success_response, error_response
from apps.weather.models import WeatherCache
from apps.weather.services import fetch_openweather_data

logger = logging.getLogger(__name__)


class WeatherDetailView(APIView):
    """
    GET /api/v1/weather/current/?lat=X&lng=Y&city=CityName&refresh=true

    Fetches current weather details, 5–7 day forecast, and agricultural alerts.
    Supports coordinates or city name. Defaults to Coimbatore (11.02, 76.96).
    Caching is applied (rounded to 2 decimal places, 30-min TTL).
    """

    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get("city") or request.query_params.get("q")
        if city:
            city = city.strip()

        force_refresh = request.query_params.get("refresh", "false").lower() in ["true", "1"]

        lat_raw = request.query_params.get("lat")
        lng_raw = request.query_params.get("lng")

        if lat_raw is not None and lng_raw is not None:
            try:
                lat = round(float(lat_raw), 2)
                lng = round(float(lng_raw), 2)
                if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                    lat, lng = 11.02, 76.96
            except (TypeError, ValueError):
                lat, lng = 11.02, 76.96
        else:
            # Default to Coimbatore if no coordinates supplied
            lat, lng = 11.02, 76.96

        # Check Cache if not forcing refresh and not custom city
        cache_entry = None
        if not force_refresh and not city:
            cache_entry = WeatherCache.objects.filter(lat=lat, lng=lng).first()
            if cache_entry and not cache_entry.is_expired():
                logger.debug("Weather cache hit for (%s, %s)", lat, lng)
                return success_response(
                    data=cache_entry.data,
                    message="Weather details (cached).",
                )

        # Cache miss, expired, or custom city — fetch new data
        logger.debug("Weather fetch for (%s, %s, city=%s)", lat, lng, city)
        weather_data = fetch_openweather_data(lat=lat, lng=lng, city=city)

        # Save to Cache if standard coordinates
        if not city:
            WeatherCache.objects.update_or_create(
                lat=lat,
                lng=lng,
                defaults={"data": weather_data, "fetched_at": timezone.now()},
            )

        return success_response(
            data=weather_data,
            message="Weather and agricultural alerts retrieved successfully.",
        )
