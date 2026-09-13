"""
Agri Link — Chat Views
========================
"""

import logging
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.core.exceptions import ResourceNotFoundError, PermissionDeniedError
from apps.core.utils import success_response, error_response, upload_to_cloudinary, StandardPagination
from apps.chat.models import ChatRoom, Message
from apps.chat.serializers import ChatRoomSerializer, MessageSerializer, MessageCreateSerializer

logger = logging.getLogger(__name__)


# ============================================================
# Chat Rooms (Create/List)
# ============================================================

class ChatRoomView(APIView):
    """
    GET  /api/v1/chat/rooms/        — List all conversation rooms for the user
    POST /api/v1/chat/rooms/        — Open/create a chat room with a recipient
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        rooms = ChatRoom.objects.filter(
            Q(user_one=user) | Q(user_two=user)
        ).order_by("-updated_at")

        serializer = ChatRoomSerializer(rooms, many=True, context={"request": request})
        return success_response(data=serializer.data)

    def post(self, request):
        recipient_id = request.data.get("recipient_id", "").strip()
        if not recipient_id:
            return error_response("recipient_id is required.")

        if recipient_id == str(request.user.pk):
            return error_response("You cannot open a chat room with yourself.")

        try:
            recipient = User.objects.get(pk=recipient_id, is_active=True)
        except (User.DoesNotExist, Exception):
            raise ResourceNotFoundError("Recipient user not found.")

        # Ensure unique sorting order for user_one and user_two to respect unique index
        u1, u2 = sorted([request.user, recipient], key=lambda u: str(u.pk))

        room, created = ChatRoom.objects.get_or_create(user_one=u1, user_two=u2)

        return success_response(
            data=ChatRoomSerializer(room, context={"request": request}).data,
            message="Chat room opened." if not created else "Chat room created.",
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


# ============================================================
# Accepted Jobs Only — Chat Rooms (Labour Dashboard)
# ============================================================

class AcceptedJobChatRoomsView(APIView):
    """
    GET /api/v1/chat/accepted-rooms/

    Returns chat rooms ONLY for accepted job relationships.
    - Labour sees: rooms with farmers whose jobs they accepted
    - Farmer sees: rooms with labourers who accepted their jobs

    Only rooms tied to ACCEPTED or COMPLETED jobs appear here.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.labour.models import Job
        from apps.core.constants import JobStatus, UserRole

        user = request.user
        accepted_statuses = [JobStatus.ACCEPTED, JobStatus.COMPLETED]

        if user.role == UserRole.LABOUR:
            # Labour: find all jobs where this labour was accepted
            accepted_jobs = Job.objects.filter(
                labour=user,
                status__in=accepted_statuses,
                is_active=True,
            ).select_related("farmer")
            partner_ids = [j.farmer_id for j in accepted_jobs]

        elif user.role == UserRole.FARMER:
            # Farmer: find all jobs where a labour accepted
            accepted_jobs = Job.objects.filter(
                farmer=user,
                status__in=accepted_statuses,
                is_active=True,
                labour__isnull=False,
            ).select_related("labour")
            partner_ids = [j.labour_id for j in accepted_jobs]

        else:
            return success_response(data=[], message="No accepted job chats for this role.")

        if not partner_ids:
            return success_response(data=[], message="No accepted jobs found. Chat is available after job acceptance.")

        # Find or build chat rooms for each partner
        rooms = ChatRoom.objects.filter(
            Q(user_one=user, user_two__in=partner_ids) |
            Q(user_one__in=partner_ids, user_two=user)
        ).order_by("-updated_at")

        # Auto-create missing rooms
        existing_partner_ids = set()
        for room in rooms:
            other = room.user_two if room.user_one == user else room.user_one
            existing_partner_ids.add(other.pk)

        for pid in partner_ids:
            if pid and pid not in existing_partner_ids:
                try:
                    partner = User.objects.get(pk=pid, is_active=True)
                    u1, u2 = sorted([user, partner], key=lambda u: str(u.pk))
                    ChatRoom.objects.get_or_create(user_one=u1, user_two=u2)
                except Exception as e:
                    logger.warning("Could not auto-create chat room with partner %s: %s", pid, e)

        # Re-fetch after potential creation
        rooms = ChatRoom.objects.filter(
            Q(user_one=user, user_two__in=partner_ids) |
            Q(user_one__in=partner_ids, user_two=user)
        ).order_by("-updated_at")

        serializer = ChatRoomSerializer(rooms, many=True, context={"request": request})
        return success_response(data=serializer.data)


# ============================================================
# Messages
# ============================================================

class MessageView(APIView):
    """
    GET  /api/v1/chat/rooms/<room_id>/messages/     — Get messages in a room
    POST /api/v1/chat/rooms/<room_id>/messages/     — Send a message in a room
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ChatRoom.objects.get(pk=room_id)
        except (ChatRoom.DoesNotExist, Exception):
            raise ResourceNotFoundError("Chat room not found.")

        if request.user != room.user_one and request.user != room.user_two:
            raise PermissionDeniedError("You are not a participant in this chat room.")

        # Mark incoming messages as read
        Message.objects.filter(room=room, is_read=False).exclude(
            sender=request.user
        ).update(is_read=True)

        # Fetch messages ordered by timestamp
        messages = Message.objects.filter(room=room).order_by("timestamp")

        paginator = StandardPagination()
        page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, room_id):
        try:
            room = ChatRoom.objects.get(pk=room_id)
        except (ChatRoom.DoesNotExist, Exception):
            raise ResourceNotFoundError("Chat room not found.")

        if request.user != room.user_one and request.user != room.user_two:
            raise PermissionDeniedError("You are not a participant in this chat room.")

        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        text = data.get("text", "")
        image_file = data.get("image")

        image_url = ""
        if image_file:
            try:
                image_url = upload_to_cloudinary(image_file, folder="agrilink/chat")
            except Exception as e:
                logger.error("Failed to upload chat message image: %s", e)
                return error_response("Image upload failed. Please try again.")

        message = Message.objects.create(
            room=room,
            sender=request.user,
            text=text,
            image_url=image_url,
            is_read=False,
        )

        # Trigger update of chat room updated_at
        room.save(update_fields=["updated_at"])

        # Send notification to the recipient
        recipient = room.get_recipient(request.user)
        from apps.notification.services import create_notification
        from apps.core.constants import NotificationType

        create_notification(
            user=recipient,
            notification_type=NotificationType.NEW_MESSAGE,
            title=f"New Message from {request.user.name or 'User'}",
            message=text if text else "[Image]",
            metadata={"room_id": str(room.pk)},
        )

        return success_response(
            data=MessageSerializer(message).data,
            message="Message sent.",
            status_code=status.HTTP_201_CREATED,
        )


# ============================================================
# New Messages Polling (for real-time feel without WebSockets)
# ============================================================

class NewMessagesView(APIView):
    """
    GET /api/v1/chat/rooms/<room_id>/new/?since=<timestamp>

    Returns messages newer than a given ISO timestamp.
    Used for polling-based real-time chat.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ChatRoom.objects.get(pk=room_id)
        except (ChatRoom.DoesNotExist, Exception):
            raise ResourceNotFoundError("Chat room not found.")

        if request.user != room.user_one and request.user != room.user_two:
            raise PermissionDeniedError("You are not a participant in this chat room.")

        since_str = request.query_params.get("since", "")

        if since_str:
            try:
                from django.utils.dateparse import parse_datetime
                from django.utils import timezone
                since_dt = parse_datetime(since_str)
                if since_dt and since_dt.tzinfo is None:
                    since_dt = timezone.make_aware(since_dt)
                messages = Message.objects.filter(room=room, timestamp__gt=since_dt).order_by("timestamp")
            except Exception:
                messages = Message.objects.filter(room=room).order_by("timestamp")
        else:
            # Return last 50 messages
            messages = Message.objects.filter(room=room).order_by("-timestamp")[:50]
            messages = reversed(list(messages))

        # Mark incoming messages as read
        Message.objects.filter(room=room, is_read=False).exclude(
            sender=request.user
        ).update(is_read=True)

        serializer = MessageSerializer(messages, many=True)
        return success_response(data=serializer.data)


# ============================================================
# Mark messages as read
# ============================================================

class MarkReadView(APIView):
    """
    POST /api/v1/chat/rooms/<room_id>/read/

    Mark all incoming messages in the room as read.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            room = ChatRoom.objects.get(pk=room_id)
        except (ChatRoom.DoesNotExist, Exception):
            raise ResourceNotFoundError("Chat room not found.")

        if request.user != room.user_one and request.user != room.user_two:
            raise PermissionDeniedError("You are not a participant in this chat room.")

        unread = Message.objects.filter(room=room, is_read=False).exclude(sender=request.user)
        count = unread.update(is_read=True)

        return success_response(
            data={"marked_read_count": count},
            message="Conversation marked as read.",
        )
