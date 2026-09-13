from django.urls import path
from apps.accounts.views import AdminLoginView
from apps.adminpanel import views

app_name = "adminpanel"

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="login"),
    path("dashboard/", views.AdminDashboardView.as_view(), name="dashboard"),
]
