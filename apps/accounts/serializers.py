"""
Agri Link — Account Serializers
=================================
Serializers for registration, login, profile, and authentication flows.
"""

from rest_framework import serializers
from apps.accounts.models import User
from apps.core.constants import UserRole, SUPPORTED_COUNTRY_CODES
from apps.core.validators import validate_phone_number, validate_password_strength


# ============================================================
# Phone Registration (Farmer, Labour, Equipment Owner)
# ============================================================

class PhoneRegistrationSerializer(serializers.Serializer):
    """Validates Firebase ID token + role for phone-based registration."""

    firebase_id_token = serializers.CharField(
        required=True,
        help_text="Firebase ID token received after OTP verification.",
    )
    role = serializers.ChoiceField(
        choices=[
            (UserRole.FARMER, "Farmer"),
            (UserRole.LABOUR, "Labour"),
            (UserRole.EQUIPMENT_OWNER, "Equipment Owner"),
            (UserRole.BUYER, "Buyer"),
        ],
        required=True,
    )
    name = serializers.CharField(max_length=100, required=False, default="")
    country_code = serializers.ChoiceField(
        choices=SUPPORTED_COUNTRY_CODES,
        default="+91",
        required=False,
    )


# ============================================================
# Email Registration (Buyer)
# ============================================================

class EmailRegistrationSerializer(serializers.Serializer):
    """Validates email + password for buyer registration."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
    )
    confirm_password = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_password(self, value):
        validate_password_strength(value)
        return value

    def validate_phone(self, value):
        if value:
            validate_phone_number(value)
            if User.objects.filter(phone=value).exists():
                raise serializers.ValidationError(
                    "A user with this phone number already exists."
                )
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return data


# ============================================================
# Phone Login
# ============================================================

class PhoneLoginSerializer(serializers.Serializer):
    """Validates Firebase ID token for phone login."""

    firebase_id_token = serializers.CharField(required=True)


# ============================================================
# Email Login
# ============================================================

class EmailLoginSerializer(serializers.Serializer):
    """Validates email + password for buyer login."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# ============================================================
# Admin Login
# ============================================================

class AdminLoginSerializer(serializers.Serializer):
    """Validates username + password for admin login."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# ============================================================
# Profile
# ============================================================

class UserProfileSerializer(serializers.ModelSerializer):
    """Read/write serializer for user profile."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "phone",
            "country_code",
            "email",
            "role",
            "name",
            "profile_photo_url",
            "address",
            "district",
            "state",
            "village",
            "gps_lat",
            "gps_lng",
            "is_verified",
            "profile_completion_pct",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "username",
            "role",
            "is_verified",
            "profile_completion_pct",
            "created_at",
            "updated_at",
        ]


class UserPublicSerializer(serializers.ModelSerializer):
    """Public-facing user info (no sensitive fields)."""

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "role",
            "profile_photo_url",
            "district",
            "state",
            "village",
            "gps_lat",
            "gps_lng",
            "profile_completion_pct",
        ]


# ============================================================
# Forgot / Reset Password
# ============================================================

class ForgotPasswordSerializer(serializers.Serializer):
    """Validates email for password reset request."""

    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    """Validates token + new password for password reset."""

    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password_strength(value)
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return data


# ============================================================
# Profile Photo Upload
# ============================================================

class ProfilePhotoSerializer(serializers.Serializer):
    """Validates profile photo upload."""

    photo = serializers.ImageField(required=True)


# ============================================================
# Dynamic Phone OTP Serializers
# ============================================================

class SendOTPSerializer(serializers.Serializer):
    """Validates phone number and role to generate dynamic OTP."""

    phone = serializers.CharField(required=True)
    role = serializers.ChoiceField(
        choices=[
            (UserRole.FARMER, "Farmer"),
            (UserRole.LABOUR, "Labour"),
            (UserRole.BUYER, "Buyer"),
            (UserRole.ADMIN, "Admin"),
        ],
        required=True,
    )
    purpose = serializers.ChoiceField(
        choices=["login", "register", "reset"],
        default="login",
        required=False,
    )

    def validate_phone(self, value):
        clean = value.strip().replace(" ", "").replace("-", "")
        if clean.startswith("+91"):
            digits = clean[3:]
        else:
            digits = clean
        if not digits.isdigit() or len(digits) != 10:
            raise serializers.ValidationError("Please enter a valid 10-digit Indian mobile number.")
        return "+91" + digits


class VerifyOTPSerializer(serializers.Serializer):
    """Validates phone OTP code and role."""

    phone = serializers.CharField(required=True)
    otp = serializers.CharField(required=True, min_length=4, max_length=10)
    role = serializers.ChoiceField(
        choices=[
            (UserRole.FARMER, "Farmer"),
            (UserRole.LABOUR, "Labour"),
            (UserRole.BUYER, "Buyer"),
            (UserRole.ADMIN, "Admin"),
        ],
        required=True,
    )

    def validate_phone(self, value):
        clean = value.strip().replace(" ", "").replace("-", "")
        if clean.startswith("+91"):
            digits = clean[3:]
        else:
            digits = clean
        if not digits.isdigit() or len(digits) != 10:
            raise serializers.ValidationError("Please enter a valid 10-digit Indian mobile number.")
        return "+91" + digits


# ============================================================
# Real User Registration Serializer
# ============================================================

class UserRegistrationSerializer(serializers.Serializer):
    """
    Validates complete registration for normal users (Farmer, Labour, Buyer).
    Normal users are strictly barred from registering as Admin.
    """

    name = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(max_length=15, required=True)
    email = serializers.EmailField(required=False, allow_blank=True, default="")
    password = serializers.CharField(required=True, write_only=True, min_length=6)
    confirm_password = serializers.CharField(required=True, write_only=True)
    role = serializers.ChoiceField(
        choices=[
            (UserRole.FARMER, "Farmer"),
            (UserRole.LABOUR, "Labour"),
            (UserRole.BUYER, "Buyer"),
        ],
        required=True,
        error_messages={"invalid_choice": "Invalid role selected. Admin registration is prohibited."},
    )
    district = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    state = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")

    def validate_phone(self, value):
        clean = value.strip().replace(" ", "").replace("-", "")
        if clean.startswith("+91"):
            digits = clean[3:]
        else:
            digits = clean
        if not digits.isdigit() or len(digits) != 10:
            raise serializers.ValidationError("Please enter a valid 10-digit mobile number.")
        formatted_phone = "+91" + digits

        if User.objects.filter(phone=formatted_phone).exists():
            raise serializers.ValidationError("A user with this mobile number is already registered.")
        return formatted_phone

    def validate_email(self, value):
        if value:
            clean_email = value.strip().lower()
            if User.objects.filter(email=clean_email).exists():
                raise serializers.ValidationError("A user with this email address is already registered.")
            return clean_email
        return ""

    def validate_password(self, value):
        validate_password_strength(value)
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data


# ============================================================
# Unified Login Serializer
# ============================================================

class UnifiedLoginSerializer(serializers.Serializer):
    """
    Handles login via either:
    1. Phone + OTP
    2. Phone/Email/Username + Password
    """

    role = serializers.ChoiceField(
        choices=[
            (UserRole.FARMER, "Farmer"),
            (UserRole.LABOUR, "Labour"),
            (UserRole.BUYER, "Buyer"),
            (UserRole.ADMIN, "Admin"),
        ],
        required=True,
    )
    identifier = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True, write_only=True)
    otp = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        ident = data.get("phone") or data.get("identifier") or data.get("username") or data.get("email")
        otp = data.get("otp")
        password = data.get("password")

        if not ident:
            raise serializers.ValidationError("Mobile number, email, or username is required.")

        if not otp and not password:
            raise serializers.ValidationError("Either OTP or password must be provided.")

        return data
