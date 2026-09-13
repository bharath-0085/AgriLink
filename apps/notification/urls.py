from django.urls import path
from apps.notification import views

app_name = "notification"

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notification-list"),
    path("unread-count/", views.UnreadNotificationCountView.as_view(), name="unread-count"),
    path("read-all/", views.NotificationReadAllView.as_view(), name="read-all"),
    path("<str:pk>/read/", views.NotificationReadView.as_view(), name="notification-read"),
]
