"""
Agri Link — Labour Serializers
================================
"""

from rest_framework import serializers
from apps.labour.models import LabourProfile, Job
from apps.accounts.serializers import UserPublicSerializer


class LabourProfileSerializer(serializers.ModelSerializer):
    """Serializer for labour profile CRUD."""

    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = LabourProfile
        fields = [
            "id", "user", "skills", "experience_years",
            "daily_wage", "is_available", "bio", "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]


class LabourProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating a labour profile."""

    class Meta:
        model = LabourProfile
        fields = [
            "skills", "experience_years", "daily_wage",
            "is_available", "bio",
        ]


class JobSerializer(serializers.ModelSerializer):
    """Full job details serializer."""

    farmer = UserPublicSerializer(read_only=True)
    labour = UserPublicSerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id", "farmer", "labour", "title", "description",
            "wage", "wage_type", "status", "start_date", "end_date",
            "location", "gps_lat", "gps_lng", "required_skills",
            "num_workers", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "farmer", "labour", "status", "created_at", "updated_at"]


class JobCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a job posting."""

    class Meta:
        model = Job
        fields = [
            "title", "description", "wage", "wage_type",
            "start_date", "end_date", "location", "gps_lat", "gps_lng",
            "required_skills", "num_workers",
        ]

    def validate_wage(self, value):
        if value <= 0:
            raise serializers.ValidationError("Wage must be positive.")
        return value
