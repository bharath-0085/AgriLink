"""
Agri Link — User & Auth Models
================================
Custom User model with multi-role support, auth tokens, and email verification.
"""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.core.constants import UserRole
from apps.core.models import BaseModel
from apps.core.validators import validate_phone_number


# ============================================================
# Custom User Manager
# ============================================================

class UserManager(BaseUserManager):
    """Custom manager for User model supporting phone and email creation."""

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required.")
        extra_fields.setdefault("is_active", True)
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)
        extra_fields.setdefault("is_verified", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


# ============================================================
# User Model
# ============================================================

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model supporting multiple roles:
    - Farmer (phone auth via Firebase)
    - Buyer (phone OTP or email + password)
    - Labour (phone auth via Firebase)
    - Equipment Owner (phone auth via Firebase)
    - Admin (username + password)
    """

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Auto-generated from phone or email. Used internally.",
    )
    phone = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_phone_number],
    )
    country_code = models.CharField(max_length=5, default="+91")
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.CHOICES)
    firebase_uid = models.CharField(
        max_length=128, unique=True, null=True, blank=True,
    )

    # Profile fields
    name = models.CharField(max_length=100, blank=True, default="")
    profile_photo_url = models.URLField(max_length=500, blank=True, default="")
    address = models.TextField(blank=True, default="")
    district = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=100, blank=True, default="")
    village = models.CharField(max_length=100, blank=True, default="")
    gps_lat = models.FloatField(null=True, blank=True)
    gps_lng = models.FloatField(null=True, blank=True)

    # Status
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_completion_pct = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "farmers"

    def __str__(self):
        return f"{self.name or self.username} ({self.role})"

    def get_full_name(self):
        return self.name or self.username

    def get_short_name(self):
        return self.name.split()[0] if self.name else self.username


# ============================================================
# Auth Token Model
# ============================================================

class AuthToken(models.Model):
    """
    Custom authentication token.
    Each user can have one active token. Tokens expire after 30 days.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="auth_token",
    )
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(auto_now=True)

    TOKEN_EXPIRY_DAYS = 30

    class Meta:
        db_table = "auth_tokens"

    def __str__(self):
        return f"Token for {self.user.username}"

    def is_expired(self):
        expiry = self.created_at + timedelta(days=self.TOKEN_EXPIRY_DAYS)
        return timezone.now() > expiry


# ============================================================
# Email Verification Token
# ============================================================

class EmailVerificationToken(BaseModel):
    """Token sent to buyer's email for verification."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_tokens",
    )
    token = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "email_verification_tokens"

    def is_expired(self):
        return timezone.now() > self.expires_at


# ============================================================
# Password Reset Token
# ============================================================

class PasswordResetToken(BaseModel):
    """Token for password reset flow."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )
    token = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "password_reset_tokens"

    def is_expired(self):
        return timezone.now() > self.expires_at


# ============================================================
# Phone OTP Model (Dynamic, Expiring, Single-Use)
# ============================================================

class PhoneOTP(BaseModel):
    """
    Dynamic OTP for phone verification during login and registration.
    Each OTP expires after OTP_EXPIRY_SECONDS (default 5 minutes) and is single-use.
    """

    phone = models.CharField(max_length=20, db_index=True)
    otp_code = models.CharField(max_length=10)
    purpose = models.CharField(max_length=20, default="login")  # 'login', 'register', 'reset'
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "phone_otps"
        ordering = ["-created_at"]

    def __str__(self):
        return f"OTP for {self.phone} ({self.purpose})"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self, code):
        if self.is_used:
            return False, "OTP has already been used."
        if self.is_expired():
            return False, "OTP has expired. Please request a new one."
        if self.attempts >= 5:
            return False, "Maximum verification attempts exceeded. Please request a new OTP."
        if self.otp_code != str(code).strip():
            self.attempts += 1
            self.save(update_fields=["attempts"])
            return False, "Invalid OTP code entered."
        return True, "Valid OTP"

