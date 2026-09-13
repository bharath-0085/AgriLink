"""
Agri Link — Chat Models
========================
"""

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class ChatRoom(BaseModel):
    """
    Represent a private chat room between two users.
    """

    user_one = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_rooms_as_one",
    )
    user_two = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_rooms_as_two",
    )

    class Meta:
        db_table = "chat_rooms"
        unique_together = ("user_one", "user_two")

    def __str__(self):
        return f"ChatRoom between {self.user_one.username} and {self.user_two.username}"

    def get_recipient(self, current_user):
        """Get the other user in the chat room."""
        return self.user_two if self.user_one == current_user else self.user_one


class Message(models.Model):
    """
    Message sent inside a private chat room.
    """

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    text = models.TextField(blank=True, default="")
    image_url = models.URLField(max_length=500, blank=True, default="")
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message by {self.sender.username} at {self.timestamp}"
