"""
Agri Link — Equipment Views
============================
APIs for listing equipment, booking equipment, and finding nearby equipment.
"""

import logging
from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from apps.core.authentication import OptionalTokenAuthentication
from apps.core.constants import BookingStatus, UserRole, NotificationType
from apps.core.exceptions import ResourceNotFoundError, PermissionDeniedError
from apps.core.permissions import IsFarmerOrEquipmentOwner, IsEquipmentOwner
from apps.core.utils import (
    success_response,
    error_response,
    get_nearby_users,
    upload_to_cloudinary,
    StandardPagination,
)
from apps.equipment.models import Equipment, EquipmentImage, EquipmentBooking
from apps.equipment.serializers import (
    EquipmentSerializer,
    EquipmentListSerializer,
    EquipmentBookingSerializer,
    EquipmentBookingCreateSerializer,
)

logger = logging.getLogger(__name__)


# ============================================================
# Default Equipment — shown when DB is empty (demo / guest)
# ============================================================

DEFAULT_EQUIPMENT = [
    {
        "id": "demo-1",
        "name": "Mahindra 575 DI Tractor",
        "category": "Tractor",
        "description": "47 HP 2WD tractor, ideal for ploughing and field preparation. Well-maintained, fuel-efficient.",
        "daily_rent": 2500,
        "hourly_rent": 400,
        "is_available": True,
        "location": "Coimbatore, Tamil Nadu",
        "owner_name": "Ravi Kumar",
        "images": [{"image_url": "https://images.unsplash.com/photo-1605002071-aaff1e88cf88?w=600&q=80"}],
        "distance_km": 3.2,
    },
    {
        "id": "demo-2",
        "name": "Combine Harvester",
        "category": "Harvester",
        "description": "Modern combine harvester for paddy, wheat and sunflower. Operator included. Minimum 4-hour booking.",
        "daily_rent": 5500,
        "hourly_rent": 800,
        "is_available": True,
        "location": "Tiruppur, Tamil Nadu",
        "owner_name": "Murugan Farms",
        "images": [{"image_url": "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=600&q=80"}],
        "distance_km": 12.7,
    },
    {
        "id": "demo-3",
        "name": "Rotavator (6 Feet)",
        "category": "Tiller",
        "description": "Heavy-duty 6-ft rotavator for deep soil cultivation and mixing crop residues.",
        "daily_rent": 1200,
        "hourly_rent": 200,
        "is_available": True,
        "location": "Erode, Tamil Nadu",
        "owner_name": "Selvam Agricultural Services",
        "images": [{"image_url": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=600&q=80"}],
        "distance_km": 22.1,
    },
    {
        "id": "demo-4",
        "name": "Power Sprayer (Petrol)",
        "category": "Sprayer",
        "description": "High-pressure petrol-powered field sprayer. 25-litre tank capacity, covers 2 acres/hour.",
        "daily_rent": 600,
        "hourly_rent": 100,
        "is_available": True,
        "location": "Karur, Tamil Nadu",
        "owner_name": "Arjun Rentals",
        "images": [{"image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&q=80"}],
        "distance_km": 35.5,
    },
    {
        "id": "demo-5",
        "name": "Mini Excavator JCB 3DX",
        "category": "Excavator",
        "description": "JCB 3DX backhoe loader for irrigation channel digging and land levelling work.",
        "daily_rent": 8000,
        "hourly_rent": 1200,
        "is_available": False,
        "location": "Salem, Tamil Nadu",
        "owner_name": "Karthik Heavy Equipment",
        "images": [{"image_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=600&q=80"}],
        "distance_km": 48.0,
    },
    {
        "id": "demo-6",
        "name": "Paddy Thresher",
        "category": "Thresher",
        "description": "Electric-powered paddy thresher. 500 kg/hour capacity. Reduces post-harvest losses.",
        "daily_rent": 900,
        "hourly_rent": 150,
        "is_available": True,
        "location": "Thanjavur, Tamil Nadu",
        "owner_name": "Palanisamy Co-op",
        "images": [{"image_url": "https://images.unsplash.com/photo-1473773508845-188df298d2d1?w=600&q=80"}],
        "distance_km": 60.3,
    },
]


# ============================================================
# Equipment CRUD
# ============================================================

class EquipmentViewSet(APIView):
    """
    GET  /api/v1/equipment/          — List all equipment with filter / search
    POST /api/v1/equipment/          — Create a new equipment listing
    """

    # GET is public so farmers can browse without logging in first
    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        from django.db.models import Q

        # Filters
        category = request.query_params.get("category", "").strip()
        search = request.query_params.get("search", "").strip()
        location = request.query_params.get("location", "").strip()
        availability = request.query_params.get("availability", "").strip().lower()
        if not availability:
            availability = request.query_params.get("is_available", "").strip().lower()
        max_price = request.query_params.get("max_price", "").strip() or request.query_params.get("price", "").strip()
        min_price = request.query_params.get("min_price", "").strip()
        sort = request.query_params.get("sort", "").strip().lower() or request.query_params.get("ordering", "").strip().lower()

        # owner_only only makes sense for authenticated users
        owner_only = request.query_params.get("owner_only", "false").lower() == "true"

        has_db_listings = Equipment.objects.filter(is_active=True).exists()

        if not has_db_listings:
            # Fall back to curated demo data so the page is never empty
            results = list(DEFAULT_EQUIPMENT)
            if category:
                results = [e for e in results if e.get("category", "").lower() == category.lower()]
            if search:
                s_lower = search.lower()
                results = [
                    e for e in results
                    if s_lower in e.get("name", "").lower()
                    or s_lower in e.get("description", "").lower()
                    or s_lower in e.get("category", "").lower()
                    or s_lower in e.get("location", "").lower()
                    or s_lower in e.get("owner_name", "").lower()
                ]
            if location:
                results = [e for e in results if location.lower() in e.get("location", "").lower()]
            if availability in ["true", "available", "1"]:
                results = [e for e in results if e.get("is_available") is True]
            elif availability in ["false", "unavailable", "0"]:
                results = [e for e in results if e.get("is_available") is False]
            if max_price:
                try:
                    mp = float(max_price)
                    results = [e for e in results if float(e.get("daily_rent", 0)) <= mp]
                except (ValueError, TypeError):
                    pass
            if min_price:
                try:
                    mp = float(min_price)
                    results = [e for e in results if float(e.get("daily_rent", 0)) >= mp]
                except (ValueError, TypeError):
                    pass

            if sort in ["price-asc", "price_asc"]:
                results.sort(key=lambda e: float(e.get("daily_rent", 0)))
            elif sort in ["price-desc", "price_desc"]:
                results.sort(key=lambda e: float(e.get("daily_rent", 0)), reverse=True)
            elif sort in ["dist-asc", "distance-asc", "distance"]:
                results.sort(key=lambda e: float(e.get("distance_km", 999)))
            elif sort in ["name-asc", "name_asc"]:
                results.sort(key=lambda e: e.get("name", "").lower())
            elif sort in ["name-desc", "name_desc"]:
                results.sort(key=lambda e: e.get("name", "").lower(), reverse=True)

            return success_response(
                data={"count": len(results), "results": results},
                message="Showing demo equipment listings.",
            )

        queryset = Equipment.objects.filter(is_active=True)

        if category:
            queryset = queryset.filter(category__iexact=category)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(purpose__icontains=search)
                | Q(category__icontains=search)
                | Q(location__icontains=search)
                | Q(owner__name__icontains=search)
            )

        if location:
            queryset = queryset.filter(location__icontains=location)

        if availability in ["true", "available", "1"]:
            queryset = queryset.filter(is_available=True)
        elif availability in ["false", "unavailable", "0"]:
            queryset = queryset.filter(is_available=False)

        if max_price:
            try:
                queryset = queryset.filter(daily_rent__lte=float(max_price))
            except (ValueError, TypeError):
                pass

        if min_price:
            try:
                queryset = queryset.filter(daily_rent__gte=float(min_price))
            except (ValueError, TypeError):
                pass

        if owner_only and request.user and request.user.is_authenticated:
            queryset = queryset.filter(owner=request.user)

        if sort in ["price-asc", "price_asc"]:
            queryset = queryset.order_by("daily_rent")
        elif sort in ["price-desc", "price_desc"]:
            queryset = queryset.order_by("-daily_rent")
        elif sort in ["name-asc", "name_asc"]:
            queryset = queryset.order_by("name")
        elif sort in ["name-desc", "name_desc"]:
            queryset = queryset.order_by("-name")
        else:
            queryset = queryset.order_by("-created_at")

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = EquipmentListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        # Allow Farmers or Equipment Owners to list equipment
        if request.user.role not in {UserRole.FARMER, UserRole.EQUIPMENT_OWNER}:
            raise PermissionDeniedError("Only farmers or equipment owners can list equipment.")

        serializer = EquipmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Remove uploaded_images list from validated_data
        uploaded_images = serializer.validated_data.pop("uploaded_images", [])

        # Create equipment listing
        equipment = serializer.save(owner=request.user)

        # Upload and attach images to Cloudinary
        for image_file in uploaded_images:
            try:
                img_url = upload_to_cloudinary(image_file, folder="agrilink/equipment")
                EquipmentImage.objects.create(equipment=equipment, image_url=img_url)
            except Exception as e:
                logger.error("Failed to upload equipment image: %s", e)

        return success_response(
            data=EquipmentSerializer(equipment).data,
            message="Equipment listing created successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class EquipmentDetailView(APIView):
    """
    GET    /api/v1/equipment/<id>/  — Get equipment details
    PUT    /api/v1/equipment/<id>/  — Update equipment details
    DELETE /api/v1/equipment/<id>/  — Delete equipment details
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            eq = Equipment.objects.get(pk=pk, is_active=True)
        except (Equipment.DoesNotExist, Exception):
            raise ResourceNotFoundError("Equipment not found.")
        return success_response(data=EquipmentSerializer(eq).data)

    def put(self, request, pk):
        try:
            eq = Equipment.objects.get(pk=pk, owner=request.user, is_active=True)
        except (Equipment.DoesNotExist, Exception):
            raise ResourceNotFoundError("Equipment not found or you are not the owner.")

        serializer = EquipmentSerializer(eq, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        uploaded_images = serializer.validated_data.pop("uploaded_images", [])
        updated_eq = serializer.save()

        # Upload new images if provided
        for image_file in uploaded_images:
            try:
                img_url = upload_to_cloudinary(image_file, folder="agrilink/equipment")
                EquipmentImage.objects.create(equipment=updated_eq, image_url=img_url)
            except Exception as e:
                logger.error("Failed to upload equipment image: %s", e)

        return success_response(
            data=EquipmentSerializer(updated_eq).data,
            message="Equipment listing updated.",
        )

    def delete(self, request, pk):
        try:
            eq = Equipment.objects.get(pk=pk, owner=request.user, is_active=True)
        except (Equipment.DoesNotExist, Exception):
            raise ResourceNotFoundError("Equipment not found or you are not the owner.")

        eq.is_active = False
        eq.save(update_fields=["is_active", "updated_at"])
        return success_response(message="Equipment listing deleted.")


# ============================================================
# Book Equipment
# ============================================================

class EquipmentBookView(APIView):
    """
    POST /api/v1/equipment/<id>/book/

    Rents/books an equipment. Renter can be a farmer.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            eq = Equipment.objects.get(pk=pk, is_available=True, is_active=True)
        except (Equipment.DoesNotExist, Exception):
            raise ResourceNotFoundError("Equipment not found or not available for rent.")

        if eq.owner == request.user:
            return error_response("You cannot book your own equipment.")

        serializer = EquipmentBookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        start_date = data["start_date"]
        end_date = data["end_date"]

        # Calculate booking cost
        duration = end_date - start_date
        total_hours = Decimal(duration.total_seconds() / 3600.0)
        total_days = Decimal(duration.days)

        # If booking is less than a day, charge hourly. Else, charge daily.
        if total_days < 1:
            cost = total_hours * eq.hourly_rent
        else:
            cost = total_days * eq.daily_rent

        # Create booking
        booking = EquipmentBooking.objects.create(
            equipment=eq,
            renter=request.user,
            start_date=start_date,
            end_date=end_date,
            total_cost=cost,
            status=BookingStatus.PENDING,
        )

        # Send notification to owner
        from apps.notification.services import create_notification

        create_notification(
            user=eq.owner,
            notification_type=NotificationType.EQUIPMENT_BOOKED,
            title="Equipment Booking Request",
            message=f"{request.user.name or 'A user'} requested to book your '{eq.name}'.",
        )

        return success_response(
            data=EquipmentBookingSerializer(booking).data,
            message="Booking request sent successfully.",
            status_code=status.HTTP_201_CREATED,
        )


# ============================================================
# Booking List
# ============================================================

class BookingListView(APIView):
    """
    GET /api/v1/equipment/bookings/

    List bookings for renters (bookings made) or owners (bookings received).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        mode = request.query_params.get("mode", "renter").strip().lower()

        if mode == "owner":
            queryset = EquipmentBooking.objects.filter(equipment__owner=user)
        else:
            queryset = EquipmentBooking.objects.filter(renter=user)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = EquipmentBookingSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


# ============================================================
# Booking Action (Approve / Reject / Complete)
# ============================================================

class BookingActionView(APIView):
    """
    POST /api/v1/equipment/bookings/<id>/action/

    Update booking status (accept, reject, complete).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        action = request.data.get("action", "").strip().lower()
        if action not in ["confirm", "cancel", "complete"]:
            return error_response("Invalid action. Choose 'confirm', 'cancel', or 'complete'.")

        try:
            booking = EquipmentBooking.objects.get(pk=booking_id)
        except (EquipmentBooking.DoesNotExist, Exception):
            raise ResourceNotFoundError("Booking not found.")

        user = request.user
        is_owner = booking.equipment.owner == user
        is_renter = booking.renter == user

        if action == "confirm":
            if not is_owner:
                raise PermissionDeniedError("Only the equipment owner can confirm a booking.")
            booking.status = BookingStatus.CONFIRMED
            # Mark equipment as unavailable if needed
            # booking.equipment.is_available = False
            # booking.equipment.save()

        elif action == "cancel":
            if not (is_owner or is_renter):
                raise PermissionDeniedError("You do not have permission to cancel this booking.")
            booking.status = BookingStatus.CANCELLED

        elif action == "complete":
            if not is_owner:
                raise PermissionDeniedError("Only the equipment owner can complete a booking.")
            booking.status = BookingStatus.COMPLETED

        booking.save(update_fields=["status", "updated_at"])

        # Send notification to the other party
        from apps.notification.services import create_notification
        notify_user = booking.renter if is_owner else booking.equipment.owner
        create_notification(
            user=notify_user,
            notification_type=NotificationType.ORDER_UPDATE,
            title=f"Booking {action.capitalize()}ed",
            message=f"Booking status for '{booking.equipment.name}' is now {booking.status}.",
        )

        return success_response(
            data=EquipmentBookingSerializer(booking).data,
            message=f"Booking {booking.status}.",
        )


# ============================================================
# Nearby Equipment Search
# ============================================================

class NearbyEquipmentView(APIView):
    """
    GET /api/v1/equipment/nearby/?lat=X&lng=Y&radius=50

    Search for available equipment near GPS coordinates.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            lat = float(request.query_params.get("lat", 0))
            lng = float(request.query_params.get("lng", 0))
            radius = float(request.query_params.get("radius", 50))
        except (ValueError, TypeError):
            return error_response("Invalid lat, lng, or radius parameter.")

        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return error_response("Invalid coordinates.")

        # Get available equipment listings with coordinates
        listings = Equipment.objects.filter(
            is_available=True, is_active=True,
            gps_lat__isnull=False, gps_lng__isnull=False,
        )

        nearby = get_nearby_users(listings, lat, lng, radius)

        results = []
        for eq, distance in nearby:
            serializer = EquipmentSerializer(eq)
            eq_data = serializer.data
            eq_data["distance_km"] = distance
            results.append(eq_data)

        return success_response(
            data=results,
            message=f"Found {len(results)} equipment listings nearby.",
        )
