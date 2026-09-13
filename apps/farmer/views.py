"""
Agri Link — Farmer Views
==========================
Dashboard and aggregation APIs for the farmer module.
"""

import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.core.constants import UserRole, OrderStatus, JobStatus, BookingStatus
from apps.core.permissions import IsFarmer
from apps.core.utils import success_response

logger = logging.getLogger(__name__)


class FarmerDashboardView(APIView):
    """
    GET /api/v1/farmer/dashboard/

    Returns aggregated dashboard data for the logged-in farmer:
    - Active product listings count
    - Pending orders count
    - Active jobs count
    - Equipment bookings count
    - Unread notifications count
    - Recent notifications
    """

    permission_classes = [IsAuthenticated, IsFarmer]

    def get(self, request):
        user = request.user

        # Product stats
        from apps.marketplace.models import Product, Order

        products = Product.objects.filter(farmer=user, is_active=True)
        active_listings = products.count()
        pending_orders = Order.objects.filter(
            product__farmer=user, status=OrderStatus.PENDING
        ).count()

        # Job stats
        from apps.labour.models import Job

        active_jobs = Job.objects.filter(
            farmer=user,
            status__in=[JobStatus.OPEN, JobStatus.ACCEPTED, JobStatus.IN_PROGRESS],
        ).count()

        # Equipment bookings
        from apps.equipment.models import EquipmentBooking

        equipment_bookings = EquipmentBooking.objects.filter(
            renter=user,
            status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED],
        ).count()

        # Notifications
        from apps.notification.models import Notification

        unread_notifications = Notification.objects.filter(
            user=user, is_read=False
        ).count()
        recent_notifications = Notification.objects.filter(user=user).order_by(
            "-created_at"
        )[:5]

        notification_data = [
            {
                "id": str(n.pk),
                "type": n.notification_type,
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at.isoformat(),
            }
            for n in recent_notifications
        ]

        return success_response(
            data={
                "active_listings": active_listings,
                "pending_orders": pending_orders,
                "active_jobs": active_jobs,
                "equipment_bookings": equipment_bookings,
                "unread_notifications": unread_notifications,
                "recent_notifications": notification_data,
                "profile_completion": user.profile_completion_pct,
            },
            message="Dashboard loaded.",
        )
