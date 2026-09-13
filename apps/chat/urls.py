from django.urls import path
from apps.chat import views

app_name = "chat"

urlpatterns = [
    # All rooms
    path("rooms/", views.ChatRoomView.as_view(), name="room-list"),
    # Accepted-jobs-only rooms (for Labour/Farmer dashboard chat)
    path("accepted-rooms/", views.AcceptedJobChatRoomsView.as_view(), name="accepted-rooms"),
    # Messages in a room
    path("rooms/<str:room_id>/messages/", views.MessageView.as_view(), name="message-list"),
    # New messages polling
    path("rooms/<str:room_id>/new/", views.NewMessagesView.as_view(), name="new-messages"),
    # Mark as read
    path("rooms/<str:room_id>/read/", views.MarkReadView.as_view(), name="mark-read"),
]
