"""
Agri Link — Buyer Serializers
==============================
"""

from rest_framework import serializers
from apps.accounts.models import User
from apps.accounts.serializers import UserPublicSerializer
from apps.buyer.models import BuyerProfile
from apps.core.models import Review
from apps.core.constants import ReviewType


class BuyerProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name", required=False)
    phone = serializers.CharField(source="user.phone", read_only=True)
    email = serializers.EmailField(source="user.email", required=False, allow_blank=True, allow_null=True)
    district = serializers.CharField(source="user.district", required=False, allow_blank=True)
    state = serializers.CharField(source="user.state", required=False, allow_blank=True)
    profile_completion_pct = serializers.IntegerField(source="user.profile_completion_pct", read_only=True)

    class Meta:
        model = BuyerProfile
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "district",
            "state",
            "company_name",
            "business_type",
            "interest_categories",
            "profile_completion_pct",
        ]
        read_only_fields = ["id", "phone", "profile_completion_pct"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user

        if "name" in user_data:
            user.name = user_data["name"]
        if "email" in user_data:
            user.email = user_data["email"]
        if "district" in user_data:
            user.district = user_data["district"]
        if "state" in user_data:
            user.state = user_data["state"]
        user.save()

        instance.company_name = validated_data.get("company_name", instance.company_name)
        instance.business_type = validated_data.get("business_type", instance.business_type)
        instance.interest_categories = validated_data.get("interest_categories", instance.interest_categories)
        instance.save()
        return instance


class BuyerReviewSerializer(serializers.ModelSerializer):
    reviewer = UserPublicSerializer(read_only=True)
    reviewee_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "reviewer",
            "reviewee",
            "reviewee_name",
            "target_id",
            "review_type",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at"]

    def get_reviewee_name(self, obj):
        if obj.reviewee:
            return obj.reviewee.name or obj.reviewee.username
        return "Farmer Partner"

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
