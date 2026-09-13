from django.urls import path
from apps.farmer import views

app_name = "farmer"

urlpatterns = [
    path("dashboard/", views.FarmerDashboardView.as_view(), name="dashboard"),
]
