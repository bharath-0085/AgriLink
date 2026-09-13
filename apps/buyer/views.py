"""
Agri Link — Buyer Views
========================
APIs for buyers to browse, search, purchase crops, manage profile and reviews.
"""

import logging
from decimal import Decimal

from django.db.models import Sum
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.buyer.models import BuyerProfile
from apps.buyer.serializers import BuyerProfileSerializer, BuyerReviewSerializer
from apps.core.constants import OrderStatus, ReviewType
from apps.core.models import Review
from apps.core.permissions import IsBuyer
from apps.core.utils import success_response, error_response, StandardPagination
from apps.marketplace.models import Order, Bookmark, Product
from apps.marketplace.serializers import ProductListSerializer, OrderSerializer
from apps.notification.models import Notification

logger = logging.getLogger(__name__)


class BuyerDashboardView(APIView):
    """
    GET /api/v1/buyer/dashboard/

    Buyer dashboard summary with live metrics, recent orders, and marketplace crops.
    """

    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        user = request.user

        # Orders metrics
        buyer_orders = Order.objects.filter(buyer=user)
        total_orders = buyer_orders.count()

        active_statuses = [OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.SHIPPED]
        active_orders = buyer_orders.filter(status__in=active_statuses).count()
        pending_orders = buyer_orders.filter(status=OrderStatus.PENDING).count()
        completed_orders = buyer_orders.filter(status=OrderStatus.DELIVERED).count()

        # Total sourced (kg) from non-cancelled orders
        valid_orders = buyer_orders.exclude(status=OrderStatus.CANCELLED)
        total_sourced_sum = valid_orders.aggregate(total_kg=Sum("quantity"))["total_kg"] or Decimal("0")
        total_sourced = float(total_sourced_sum)

        # Total payments (₹)
        total_payments_sum = valid_orders.aggregate(total_amt=Sum("total_price"))["total_amt"] or Decimal("0")
        total_payments = float(total_payments_sum)

        # Bookmarks & Notifications
        bookmarks_count = Bookmark.objects.filter(user=user).count()
        unread_notifications = Notification.objects.filter(user=user, is_read=False).count()

        # Available crops in marketplace
        available_crops_count = Product.objects.filter(is_active=True, is_available=True).count()

        # Recent orders (latest 5)
        recent_orders_qs = buyer_orders.order_by("-created_at")[:5]
        recent_orders_data = OrderSerializer(recent_orders_qs, many=True).data

        # Recent crops (latest 4 for quick highlights)
        recent_crops_qs = Product.objects.filter(is_active=True, is_available=True).order_by("-created_at")[:4]
        recent_crops_data = ProductListSerializer(recent_crops_qs, many=True).data

        # Buyer profile
        buyer_profile, _ = BuyerProfile.objects.get_or_create(user=user)
        profile_data = BuyerProfileSerializer(buyer_profile).data

        return success_response(
            data={
                "active_orders": active_orders,
                "total_orders": total_orders,
                "pending_orders": pending_orders,
                "completed_orders": completed_orders,
                "total_sourced": total_sourced,
                "total_payments": total_payments,
                "bookmarks_count": bookmarks_count,
                "unread_notifications": unread_notifications,
                "available_crops_count": available_crops_count,
                "recent_orders": recent_orders_data,
                "recent_crops": recent_crops_data,
                "profile": profile_data,
            },
            message="Buyer dashboard metrics loaded.",
        )


class BrowseCropsView(APIView):
    """
    GET /api/v1/buyer/crops/

    Browse available crops with optional search and filters.
    Query params: search, min_price, max_price, location
    """

    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        queryset = Product.objects.filter(is_active=True, is_available=True)

        # Search by crop name
        search = request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(crop_name__icontains=search)

        # Filter by price range
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except (ValueError, TypeError):
                pass
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except (ValueError, TypeError):
                pass

        # Filter by location (district)
        location = request.query_params.get("location", "").strip()
        if location:
            queryset = queryset.filter(location__icontains=location)

        queryset = queryset.order_by("-created_at")

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class BuyerProfileView(APIView):
    """
    GET  /api/v1/buyer/profile/  — Retrieve current buyer profile
    PUT  /api/v1/buyer/profile/  — Update buyer profile
    """

    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        profile, _ = BuyerProfile.objects.get_or_create(user=request.user)
        serializer = BuyerProfileSerializer(profile)
        return success_response(data=serializer.data)

    def put(self, request):
        profile, _ = BuyerProfile.objects.get_or_create(user=request.user)
        serializer = BuyerProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_profile = serializer.save()
        return success_response(
            data=BuyerProfileSerializer(updated_profile).data,
            message="Buyer profile updated successfully.",
        )


class BuyerReviewView(APIView):
    """
    GET  /api/v1/buyer/reviews/  — List reviews submitted by the buyer
    POST /api/v1/buyer/reviews/  — Post a new review for a farmer/product
    """

    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        reviews = Review.objects.filter(reviewer=request.user, is_active=True).order_by("-created_at")
        serializer = BuyerReviewSerializer(reviews, many=True)
        return success_response(data=serializer.data)

    def post(self, request):
        data = request.data.copy()
        reviewee_id = data.get("reviewee_id") or data.get("farmer_id")
        target_id = data.get("target_id", "")
        rating = data.get("rating", 5)
        comment = data.get("comment", "").strip()

        reviewee = None
        if reviewee_id:
            reviewee = User.objects.filter(id=reviewee_id).first()

        review = Review.objects.create(
            reviewer=request.user,
            reviewee=reviewee,
            target_id=str(target_id),
            review_type=ReviewType.FARMER if reviewee else ReviewType.PRODUCT,
            rating=int(rating),
            comment=comment,
        )

        return success_response(
            data=BuyerReviewSerializer(review).data,
            message="Review submitted successfully. Thank you for your feedback!",
            status_code=status.HTTP_201_CREATED,
        )
