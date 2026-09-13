"""
Agri Link — Marketplace Views
==============================
APIs for posting crops, purchasing crops, browsing, and bookmarking.
"""

import logging
from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from apps.core.authentication import OptionalTokenAuthentication
from apps.core.constants import OrderStatus, UserRole, NotificationType
from apps.core.exceptions import ResourceNotFoundError, PermissionDeniedError
from apps.core.permissions import IsFarmer, IsBuyer
from apps.core.utils import (
    success_response,
    error_response,
    upload_to_cloudinary,
    StandardPagination,
    get_nearby_users,
)
from apps.marketplace.models import Product, ProductImage, Order, Bookmark
from apps.marketplace.serializers import (
    ProductSerializer,
    ProductListSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    BookmarkSerializer,
)

logger = logging.getLogger(__name__)


# ============================================================
# Product CRUD
# ============================================================

class ProductViewSet(APIView):
    """
    GET  /api/v1/marketplace/          — List crops (with search / filter)
    POST /api/v1/marketplace/          — Add a new crop listing (Farmer only)
    """

    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = Product.objects.filter(is_active=True, is_available=True)

        # Apply search and filters
        search = request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(crop_name__icontains=search)

        location = request.query_params.get("location", "").strip()
        if location:
            queryset = queryset.filter(location__icontains=location)

        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        if min_price:
            try:
                queryset = queryset.filter(price__gte=Decimal(min_price))
            except (ValueError, TypeError):
                pass
        if max_price:
            try:
                queryset = queryset.filter(price__lte=Decimal(max_price))
            except (ValueError, TypeError):
                pass

        farmer_only = request.query_params.get("farmer_only", "false").lower() == "true"
        if farmer_only:
            if not request.user.is_authenticated:
                raise PermissionDeniedError("Authentication required to view your crops.")
            queryset = queryset.filter(farmer=request.user)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if request.user.role != UserRole.FARMER:
            raise PermissionDeniedError("Only farmers can list crops on the marketplace.")

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_images = serializer.validated_data.pop("uploaded_images", [])

        # Save listing
        product = serializer.save(farmer=request.user)

        # Upload images to Cloudinary
        for image_file in uploaded_images:
            try:
                img_url = upload_to_cloudinary(image_file, folder="agrilink/crops")
                ProductImage.objects.create(product=product, image_url=img_url)
            except Exception as e:
                logger.error("Failed to upload crop image: %s", e)

        return success_response(
            data=ProductSerializer(product).data,
            message="Crop listed successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class ProductDetailView(APIView):
    """
    GET    /api/v1/marketplace/<id>/   — View crop details
    PUT    /api/v1/marketplace/<id>/   — Update crop details (Farmer owner only)
    DELETE /api/v1/marketplace/<id>/   — Soft delete crop details (Farmer owner only)
    """

    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            prod = Product.objects.get(pk=pk, is_active=True)
        except (Product.DoesNotExist, Exception):
            raise ResourceNotFoundError("Crop listing not found.")
        return success_response(data=ProductSerializer(prod).data)

    def put(self, request, pk):
        try:
            prod = Product.objects.get(pk=pk, farmer=request.user, is_active=True)
        except (Product.DoesNotExist, Exception):
            raise ResourceNotFoundError("Crop listing not found or you are not the owner.")

        serializer = ProductSerializer(prod, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        uploaded_images = serializer.validated_data.pop("uploaded_images", [])
        updated_prod = serializer.save()

        # Upload new images if provided
        for image_file in uploaded_images:
            try:
                img_url = upload_to_cloudinary(image_file, folder="agrilink/crops")
                ProductImage.objects.create(product=updated_prod, image_url=img_url)
            except Exception as e:
                logger.error("Failed to upload crop image: %s", e)

        return success_response(
            data=ProductSerializer(updated_prod).data,
            message="Crop listing updated.",
        )

    def delete(self, request, pk):
        try:
            prod = Product.objects.get(pk=pk, farmer=request.user, is_active=True)
        except (Product.DoesNotExist, Exception):
            raise ResourceNotFoundError("Crop listing not found or you are not the owner.")

        prod.is_active = False
        prod.save(update_fields=["is_active", "updated_at"])
        return success_response(message="Crop listing deleted.")


# ============================================================
# Order / Purchase Crops
# ============================================================

class OrderCreateView(APIView):
    """
    POST /api/v1/marketplace/<id>/order/

    Buyer orders/purchases a crop.
    """

    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request, pk):
        try:
            prod = Product.objects.get(pk=pk, is_available=True, is_active=True)
        except (Product.DoesNotExist, Exception):
            raise ResourceNotFoundError("Crop listing not found or not available.")

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        req_qty = Decimal(serializer.validated_data["quantity"])

        if req_qty > prod.quantity:
            return error_response(
                f"Requested quantity exceeds available stock ({prod.quantity} {prod.unit} available)."
            )

        # Calculate price
        total_price = req_qty * prod.price

        # Update product stock
        prod.quantity -= req_qty
        if prod.quantity == 0:
            prod.is_available = False
        prod.save(update_fields=["quantity", "is_available"])

        # Create Order
        order = Order.objects.create(
            product=prod,
            buyer=request.user,
            quantity=req_qty,
            total_price=total_price,
            status=OrderStatus.PENDING,
        )

        # Send notification to farmer
        from apps.notification.services import create_notification

        create_notification(
            user=prod.farmer,
            notification_type=NotificationType.BUYER_INTERESTED,
            title="New Crop Order Received",
            message=f"{request.user.name or 'A buyer'} ordered {req_qty} {prod.unit} of your '{prod.crop_name}'.",
        )

        return success_response(
            data=OrderSerializer(order).data,
            message="Order placed successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class OrderListView(APIView):
    """
    GET /api/v1/marketplace/orders/

    List orders.
    Query param: role=buyer (own purchases) or role=farmer (sales)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = request.query_params.get("role", "buyer").strip().lower()

        if role == "farmer":
            queryset = Order.objects.filter(product__farmer=user)
        else:
            queryset = Order.objects.filter(buyer=user)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OrderSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class OrderActionView(APIView):
    """
    POST /api/v1/marketplace/orders/<id>/action/

    Update crop order status (confirm, cancel, ship, deliver).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        action = request.data.get("action", "").strip().lower()
        if action not in ["confirm", "cancel", "ship", "deliver"]:
            return error_response("Invalid action. Choose 'confirm', 'cancel', 'ship', or 'deliver'.")

        try:
            order = Order.objects.get(pk=order_id)
        except (Order.DoesNotExist, Exception):
            raise ResourceNotFoundError("Order not found.")

        user = request.user
        is_farmer = order.product.farmer == user
        is_buyer = order.buyer == user

        if action == "confirm":
            if not is_farmer:
                raise PermissionDeniedError("Only the farmer who listed the crop can confirm the order.")
            order.status = OrderStatus.CONFIRMED

        elif action == "cancel":
            if not (is_farmer or is_buyer):
                raise PermissionDeniedError("You do not have permission to cancel this order.")

            # Return stock back to product
            order.product.quantity += order.quantity
            order.product.is_available = True
            order.product.save(update_fields=["quantity", "is_available"])

            order.status = OrderStatus.CANCELLED

        elif action == "ship":
            if not is_farmer:
                raise PermissionDeniedError("Only the farmer can mark the order as shipped.")
            order.status = OrderStatus.SHIPPED

        elif action == "deliver":
            if not is_farmer:
                raise PermissionDeniedError("Only the farmer can mark the order as delivered.")
            order.status = OrderStatus.DELIVERED

        order.save(update_fields=["status", "updated_at"])

        # Send notification to the other party
        from apps.notification.services import create_notification
        notify_user = order.buyer if is_farmer else order.product.farmer
        create_notification(
            user=notify_user,
            notification_type=NotificationType.ORDER_UPDATE,
            title=f"Order {action.capitalize()}ed",
            message=f"Order for '{order.product.crop_name}' is now {order.status}.",
        )

        return success_response(
            data=OrderSerializer(order).data,
            message=f"Order status updated to {order.status}.",
        )


# ============================================================
# Bookmarks
# ============================================================

class BookmarkView(APIView):
    """
    GET  /api/v1/marketplace/bookmarks/        — List buyer's bookmarked crops
    POST /api/v1/marketplace/bookmarks/        — Add / remove a crop bookmark
    """

    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        queryset = Bookmark.objects.filter(user=request.user).order_by("-created_at")
        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = BookmarkSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product_id", "").strip()
        if not product_id:
            return error_response("product_id is required.")

        try:
            prod = Product.objects.get(pk=product_id, is_active=True)
        except (Product.DoesNotExist, Exception):
            raise ResourceNotFoundError("Crop listing not found.")

        bookmark, created = Bookmark.objects.get_or_create(user=request.user, product=prod)

        if not created:
            bookmark.delete()
            return success_response(message="Bookmark removed successfully.")

        return success_response(
            data=BookmarkSerializer(bookmark).data,
            message="Bookmark added successfully.",
            status_code=status.HTTP_201_CREATED,
        )


# ============================================================
# GPS Nearby Buyers / Farmers Search
# ============================================================

class NearbyFarmersBuyersView(APIView):
    """
    GET /api/v1/marketplace/nearby/?role=farmer&lat=X&lng=Y&radius=50

    Search for farmers or buyers nearby based on GPS.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.query_params.get("role", "farmer").strip().lower()
        if role not in ["farmer", "buyer"]:
            return error_response("Invalid role parameter. Choose 'farmer' or 'buyer'.")

        try:
            lat = float(request.query_params.get("lat", 0))
            lng = float(request.query_params.get("lng", 0))
            radius = float(request.query_params.get("radius", 50))
        except (ValueError, TypeError):
            return error_response("Invalid lat, lng, or radius parameter.")

        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return error_response("Invalid coordinates.")

        from apps.accounts.models import User
        from apps.accounts.serializers import UserPublicSerializer

        users = User.objects.filter(
            role=role, is_active=True,
            gps_lat__isnull=False, gps_lng__isnull=False,
        )

        nearby = get_nearby_users(users, lat, lng, radius)

        results = []
        for user, distance in nearby:
            user_data = UserPublicSerializer(user).data
            user_data["distance_km"] = distance
            results.append(user_data)

        return success_response(
            data=results,
            message=f"Found {len(results)} {role}s nearby.",
        )
