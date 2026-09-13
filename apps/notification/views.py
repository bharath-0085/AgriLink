"""
Agri Link — Notification Views
===============================
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.core.exceptions import ResourceNotFoundError
from apps.core.utils import success_response, StandardPagination
from apps.notification.models import Notification


class NotificationListView(APIView):
    """
    GET /api/v1/notifications/

    List user's notifications (paginated, ordered by newest first).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Notification.objects.filter(user=request.user)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)

        results = [
            {
                "id": str(n.pk),
                "notification_type": n.notification_type,
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "metadata": n.metadata,
                "created_at": n.created_at.isoformat(),
            }
            for n in page
        ]

        return paginator.get_paginated_response(results)


class UnreadNotificationCountView(APIView):
    """
    GET /api/v1/notifications/unread-count/

    Return count of unread notifications.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return success_response(data={"unread_count": count})


class NotificationReadView(APIView):
    """
    POST /api/v1/notifications/<id>/read/

    Mark a notification as read.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            n = Notification.objects.get(pk=pk, user=request.user)
        except (Notification.DoesNotExist, Exception):
            raise ResourceNotFoundError("Notification not found.")

        n.is_read = True
        n.save(update_fields=["is_read", "updated_at"])
        return success_response(message="Notification marked as read.")


class NotificationReadAllView(APIView):
    """
    POST /api/v1/notifications/read-all/

    Mark all user's notifications as read.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        unread = Notification.objects.filter(user=request.user, is_read=False)
        count = unread.update(is_read=True)
        return success_response(
            data={"marked_read_count": count},
            message="All notifications marked as read.",
        )
