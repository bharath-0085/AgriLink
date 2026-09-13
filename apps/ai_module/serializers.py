"""
Agri Link — AI Module Serializers
===================================
"""

from rest_framework import serializers
from apps.core.validators import validate_image_file


class CropRecommendSerializer(serializers.Serializer):
    """
    Validate standard features required by crop recommendation models:
    N, P, K, temperature, humidity, ph, rainfall.
    """

    N = serializers.FloatField(required=True, help_text="Nitrogen content in soil (mg/kg)")
    P = serializers.FloatField(required=True, help_text="Phosphorus content in soil (mg/kg)")
    K = serializers.FloatField(required=True, help_text="Potassium content in soil (mg/kg)")
    temperature = serializers.FloatField(required=True, help_text="Air temperature (°C)")
    humidity = serializers.FloatField(required=True, help_text="Relative humidity (%)")
    ph = serializers.FloatField(required=True, help_text="Soil pH value (0 - 14)")
    rainfall = serializers.FloatField(required=True, help_text="Average rainfall (mm)")

    def validate_ph(self, value):
        if value < 0 or value > 14:
            raise serializers.ValidationError("pH must be between 0 and 14.")
        return value

    def validate_humidity(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Humidity must be between 0 and 100%.")
        return value


class DiseaseDetectSerializer(serializers.Serializer):
    """
    Validate leaf image upload.
    """

    image = serializers.ImageField(required=True, validators=[validate_image_file])


class ChatbotSerializer(serializers.Serializer):
    """
    Validate Gemini chatbot queries.
    """

    message = serializers.CharField(required=True, max_length=1000, allow_blank=False)
