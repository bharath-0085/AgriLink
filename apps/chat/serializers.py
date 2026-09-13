"""
Agri Link — Chat Serializers
=============================
"""

from rest_framework import serializers
from apps.chat.models import ChatRoom, Message
from apps.accounts.serializers import UserPublicSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    recipient = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ["id", "recipient", "last_message", "unread_count", "created_at", "updated_at"]

    def get_recipient(self, obj):
        request = self.context.get("request")
        if request and request.user:
            recipient = obj.get_recipient(request.user)
            return UserPublicSerializer(recipient).data
        return None

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-timestamp").first()
        if last_msg:
            return {
                "id": str(last_msg.pk),
                "text": last_msg.text,
                "image_url": last_msg.image_url,
                "sender_id": str(last_msg.sender_id),
                "is_read": last_msg.is_read,
                "timestamp": last_msg.timestamp.isoformat(),
            }
        return None

    def get_unread_count(self, obj):
        request = self.context.get("request")
        if request and request.user:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name", read_only=True)
    sender_photo = serializers.URLField(source="sender.profile_photo_url", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "room", "sender", "sender_name", "sender_photo",
            "text", "image_url", "is_read", "timestamp",
        ]
        read_only_fields = ["id", "room", "sender", "is_read", "timestamp"]


class MessageCreateSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, default="", allow_blank=True)
    image = serializers.ImageField(required=False, allow_empty_file=False)

    def validate(self, data):
        if not data.get("text") and not data.get("image"):
            raise serializers.ValidationError("Message must contain either text or an image.")
        return data
