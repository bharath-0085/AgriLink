from django.urls import path
from apps.equipment import views

app_name = "equipment"

urlpatterns = [
    # Equipment listing CRUD
    path("", views.EquipmentViewSet.as_view(), name="equipment-list"),
    path("<str:pk>/", views.EquipmentDetailView.as_view(), name="equipment-detail"),

    # Booking
    path("bookings/", views.BookingListView.as_view(), name="booking-list"),
    path("<str:pk>/book/", views.EquipmentBookView.as_view(), name="equipment-book"),
    path("bookings/<str:booking_id>/action/", views.BookingActionView.as_view(), name="booking-action"),

    # GPS nearby search
    path("nearby/", views.NearbyEquipmentView.as_view(), name="nearby"),
]
