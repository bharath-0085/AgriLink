from django.urls import path
from apps.buyer import views

app_name = "buyer"

urlpatterns = [
    path("dashboard/", views.BuyerDashboardView.as_view(), name="dashboard"),
    path("crops/", views.BrowseCropsView.as_view(), name="browse-crops"),
    path("profile/", views.BuyerProfileView.as_view(), name="profile"),
    path("reviews/", views.BuyerReviewView.as_view(), name="reviews"),
]
