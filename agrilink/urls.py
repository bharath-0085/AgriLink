"""
Agri Link — Root URL Configuration
====================================
All API endpoints are namespaced under /api/v1/.
Admin panel is at /admin-login/ (not visible on homepage).
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings

from apps.ai_module.api_assistant import AIAssistantChatAPIView

urlpatterns = [
    # ---- Admin Dashboard route ----
    path("admin/dashboard", TemplateView.as_view(template_name="admin_dashboard.html"), name="admin-dashboard-route"),
    path("admin/dashboard/", TemplateView.as_view(template_name="admin_dashboard.html"), name="admin-dashboard-route-slash"),

    # ---- Django built-in admin (hidden) ----
    path("admin/", admin.site.urls),

    # ---- Custom admin panel ----
    path("admin-login/", include("apps.adminpanel.urls")),

    # ---- Dedicated AI Assistant API Endpoint ----
    path("api/ai-assistant/chat", AIAssistantChatAPIView.as_view(), name="api-ai-assistant-chat"),
    path("api/ai-assistant/chat/", AIAssistantChatAPIView.as_view(), name="api-ai-assistant-chat-slash"),

    # ---- API v1 ----
    path("api/v1/accounts/", include("apps.accounts.urls")),
    path("api/v1/farmer/", include("apps.farmer.urls")),
    path("api/v1/buyer/", include("apps.buyer.urls")),
    path("api/v1/labour/", include("apps.labour.urls")),
    path("api/v1/equipment/", include("apps.equipment.urls")),
    path("api/v1/marketplace/", include("apps.marketplace.urls")),
    path("api/v1/weather/", include("apps.weather.urls")),
    path("api/v1/chat/", include("apps.chat.urls")),
    path("api/v1/notifications/", include("apps.notification.urls")),
    path("api/v1/ai/", include("apps.ai_module.urls")),

    # ---- Frontend SPA & Pages serving ----
    path("", TemplateView.as_view(template_name="index.html"), name="frontend-home"),
    path("index.html", TemplateView.as_view(template_name="index.html"), name="frontend-home-alias"),
    path("about", TemplateView.as_view(template_name="about.html"), name="about"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about-slash"),
    path("about.html", TemplateView.as_view(template_name="about.html"), name="about-html"),
    path("login", TemplateView.as_view(template_name="login.html"), name="login"),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login-slash"),
    path("login.html", TemplateView.as_view(template_name="login.html"), name="login-html"),
    path("register", TemplateView.as_view(template_name="login.html"), name="register"),
    path("register/", TemplateView.as_view(template_name="login.html"), name="register-slash"),
    path("farmer_dashboard.html", TemplateView.as_view(template_name="farmer_dashboard.html"), name="farmer-dashboard"),
    path("labour_dashboard.html", TemplateView.as_view(template_name="labour_dashboard.html"), name="labour-dashboard"),
    path("buyer_dashboard.html", TemplateView.as_view(template_name="buyer_dashboard.html"), name="buyer-dashboard"),
    path("admin_dashboard.html", TemplateView.as_view(template_name="admin_dashboard.html"), name="admin-dashboard"),
    path("farmer/dashboard", TemplateView.as_view(template_name="farmer_dashboard.html"), name="farmer-dashboard-route"),
    path("farmer/dashboard/", TemplateView.as_view(template_name="farmer_dashboard.html"), name="farmer-dashboard-route-slash"),
    path("labour/dashboard", TemplateView.as_view(template_name="labour_dashboard.html"), name="labour-dashboard-route"),
    path("labour/dashboard/", TemplateView.as_view(template_name="labour_dashboard.html"), name="labour-dashboard-route-slash"),
    path("buyer/dashboard", TemplateView.as_view(template_name="buyer_dashboard.html"), name="buyer-dashboard-route"),
    path("buyer/dashboard/", TemplateView.as_view(template_name="buyer_dashboard.html"), name="buyer-dashboard-route-slash"),

    # ---- Dedicated AI Assistant Route ----
    path("ai-assistant", TemplateView.as_view(template_name="ai_assistant.html"), name="ai-assistant-page"),
    path("ai-assistant/", TemplateView.as_view(template_name="ai_assistant.html"), name="ai-assistant-page-slash"),
    path("ai_assistant.html", TemplateView.as_view(template_name="ai_assistant.html"), name="ai-assistant-html"),

    # ---- Static Assets Serving ----
    re_path(r"^(?:about/|login/|register/|farmer/|labour/|buyer/|admin/|ai-assistant/)?components/(?P<path>.*)$", serve, {"document_root": settings.BASE_DIR / "frontend/components"}),
    re_path(r"^(?:about/|login/|register/|farmer/|labour/|buyer/|admin/|ai-assistant/)?css/(?P<path>.*)$", serve, {"document_root": settings.BASE_DIR / "frontend/css"}),
    re_path(r"^(?:about/|login/|register/|farmer/|labour/|buyer/|admin/|ai-assistant/)?js/(?P<path>.*)$", serve, {"document_root": settings.BASE_DIR / "frontend/js"}),
    re_path(r"^(?:about/|login/|register/|farmer/|labour/|buyer/|admin/|ai-assistant/)?images/(?P<path>.*)$", serve, {"document_root": settings.BASE_DIR / "frontend/images"}),
]


