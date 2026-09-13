"""
Agri Link — Admin Panel Views
==============================
Dashboard and metric views for the admin panel.
"""

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.core.constants import UserRole
from apps.core.permissions import IsAdmin
from apps.core.utils import success_response

logger = logging.getLogger(__name__)


class AdminDashboardView(APIView):
    """
    GET /admin-login/dashboard/

    Returns metrics for the admin panel:
    - User breakdowns by role
    - Total listings (crops & equipment)
    - Total transaction summaries
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        # User counts
        farmers_count = User.objects.filter(role=UserRole.FARMER, is_active=True).count()
        buyers_count = User.objects.filter(role=UserRole.BUYER, is_active=True).count()
        labourers_count = User.objects.filter(role=UserRole.LABOUR, is_active=True).count()
        owners_count = User.objects.filter(role=UserRole.EQUIPMENT_OWNER, is_active=True).count()
        admins_count = User.objects.filter(role=UserRole.ADMIN, is_active=True).count()

        # Listings
        from apps.marketplace.models import Product, Order
        total_crops = Product.objects.filter(is_active=True).count()
        total_orders = Order.objects.count()

        from apps.equipment.models import Equipment, EquipmentBooking
        total_equipment = Equipment.objects.filter(is_active=True).count()
        total_bookings = EquipmentBooking.objects.count()

        from apps.labour.models import Job
        total_jobs = Job.objects.filter(is_active=True).count()

        return success_response(
            data={
                "users": {
                    "farmers": farmers_count,
                    "buyers": buyers_count,
                    "labourers": labourers_count,
                    "equipment_owners": owners_count,
                    "admins": admins_count,
                    "total": farmers_count + buyers_count + labourers_count + owners_count + admins_count,
                },
                "marketplace": {
                    "total_crop_listings": total_crops,
                    "total_orders": total_orders,
                },
                "rentals": {
                    "total_equipment_listings": total_equipment,
                    "total_bookings": total_bookings,
                },
                "labour_jobs": {
                    "total_jobs": total_jobs,
                },
            },
            message="Admin dashboard statistics retrieved successfully.",
        )
