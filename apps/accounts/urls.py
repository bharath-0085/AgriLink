"""
Agri Link — Account URL Routing
=================================
"""

from django.urls import path
from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    # Dynamic Phone OTP
    path("otp/send/", views.SendOTPView.as_view(), name="otp-send"),
    path("otp/verify/", views.VerifyOTPView.as_view(), name="otp-verify"),

    # Unified Registration & Login
    path("register/", views.UnifiedRegisterView.as_view(), name="register-unified"),
    path("login/", views.UnifiedLoginView.as_view(), name="login-unified"),

    # Legacy / Role-specific Registration
    path("register/phone/", views.PhoneRegistrationView.as_view(), name="register-phone"),
    path("register/email/", views.EmailRegistrationView.as_view(), name="register-email"),

    # Legacy / Role-specific Login
    path("login/phone/", views.PhoneLoginView.as_view(), name="login-phone"),
    path("login/email/", views.EmailLoginView.as_view(), name="login-email"),

    # Email verification
    path("verify-email/", views.VerifyEmailView.as_view(), name="verify-email"),

    # Password management
    path("forgot-password/", views.ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),

    # Profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/photo/", views.ProfilePhotoView.as_view(), name="profile-photo"),

    # Password management
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),

    # Logout
    path("logout/", views.LogoutView.as_view(), name="logout"),
]

