"""
Agri Link — Marketplace Serializers
====================================
"""

from rest_framework import serializers
from apps.marketplace.models import Product, ProductImage, Order, Bookmark
from apps.accounts.serializers import UserPublicSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image_url"]


class ProductSerializer(serializers.ModelSerializer):
    farmer = UserPublicSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "id", "farmer", "crop_name", "quantity", "unit", "price",
            "harvest_date", "location", "gps_lat", "gps_lng", "description",
            "is_available", "images", "uploaded_images", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "farmer", "images", "created_at", "updated_at"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    farmer = UserPublicSerializer(read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "farmer", "crop_name", "quantity", "unit", "price",
            "location", "harvest_date", "first_image",
        ]

    def get_first_image(self, obj):
        img = obj.images.first()
        return img.image_url if img else None


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    buyer = UserPublicSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "product", "buyer", "quantity", "total_price",
            "status", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "product", "buyer", "total_price", "status", "created_at", "updated_at"]


class OrderCreateSerializer(serializers.Serializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    delivery_address = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Order quantity must be greater than zero.")
        return value


class BookmarkSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "product", "created_at"]
        read_only_fields = ["id", "created_at"]
