from django.urls import path
from apps.weather import views

app_name = "weather"

urlpatterns = [
    path("current/", views.WeatherDetailView.as_view(), name="current-weather"),
]
