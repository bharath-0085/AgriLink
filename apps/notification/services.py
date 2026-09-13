"""
Agri Link — Notification Service
=================================
Utility functions to create notifications programmatically across apps.
"""

import logging

from apps.core.constants import NotificationType
from apps.notification.models import Notification

logger = logging.getLogger(__name__)


def create_notification(user, title, message, notification_type=NotificationType.GENERAL, metadata=None):
    """
    Create a notification for a user.

    Args:
        user: The User instance to notify.
        title (str): Title of the notification.
        message (str): Text content of the notification.
        notification_type (str): Type matching NotificationType choices.
        metadata (dict, optional): Custom metadata JSON fields.

    Returns:
        Notification: The created notification object.
    """
    if metadata is None:
        metadata = {}

    try:
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            metadata=metadata,
        )
        logger.debug(
            "Created notification id=%s for user=%s type=%s",
            notification.id,
            user.username,
            notification_type,
        )
        return notification
    except Exception as e:
        logger.error(
            "Failed to create notification for user %s: %s",
            user.username,
            e,
        )
        return None
