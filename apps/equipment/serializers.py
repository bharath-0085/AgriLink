"""
Agri Link — Equipment Serializers
==================================
"""

from rest_framework import serializers
from apps.equipment.models import Equipment, EquipmentImage, EquipmentBooking
from apps.accounts.serializers import UserPublicSerializer


class EquipmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentImage
        fields = ["id", "image_url"]


class EquipmentSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(read_only=True)
    images = EquipmentImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Equipment
        fields = [
            "id", "owner", "name", "category", "purpose", "description",
            "hourly_rent", "daily_rent", "is_available", "location",
            "gps_lat", "gps_lng", "images", "uploaded_images",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner", "images", "created_at", "updated_at"]

    def validate(self, data):
        if data.get("gps_lat") is not None and data.get("gps_lng") is None:
            raise serializers.ValidationError("Longitude is required if latitude is provided.")
        if data.get("gps_lng") is not None and data.get("gps_lat") is None:
            raise serializers.ValidationError("Latitude is required if longitude is provided.")
        return data


class EquipmentListSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = [
            "id", "owner", "name", "category", "hourly_rent", "daily_rent",
            "is_available", "location", "gps_lat", "gps_lng", "first_image",
        ]

    def get_first_image(self, obj):
        img = obj.images.first()
        return img.image_url if img else None


class EquipmentBookingSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(read_only=True)
    renter = UserPublicSerializer(read_only=True)

    class Meta:
        model = EquipmentBooking
        fields = [
            "id", "equipment", "renter", "start_date", "end_date",
            "status", "total_cost", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "equipment", "renter", "total_cost", "status", "created_at", "updated_at"]


class EquipmentBookingCreateSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)

    def validate(self, data):
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError("End date must be after start date.")
        import django.utils.timezone
        if data["start_date"] < django.utils.timezone.now():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return data
