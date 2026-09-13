"""
Agri Link — Account Views
===========================
API views for registration, login, profile, email verification, and password reset.
"""

import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, logout as django_logout
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.authentication import TokenAuthentication

from apps.accounts.models import (
    AuthToken,
    EmailVerificationToken,
    PasswordResetToken,
    PhoneOTP,
    User,
)
from apps.accounts.serializers import (
    AdminLoginSerializer,
    EmailLoginSerializer,
    EmailRegistrationSerializer,
    ForgotPasswordSerializer,
    PhoneLoginSerializer,
    PhoneRegistrationSerializer,
    ProfilePhotoSerializer,
    ResetPasswordSerializer,
    SendOTPSerializer,
    UnifiedLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    VerifyOTPSerializer,
)
from apps.core.constants import UserRole
from apps.core.sms import SMSService
from apps.core.exceptions import (
    InvalidCredentialsError,
    InvalidFirebaseTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
    EmailNotVerifiedError,
)
from apps.core.utils import (
    calculate_profile_completion,
    generate_auth_token,
    generate_verification_token,
    success_response,
    error_response,
    upload_to_cloudinary,
)

logger = logging.getLogger(__name__)


def get_dashboard_redirect(role: str) -> str:
    """Return correct dashboard redirect URL based on verified user role."""
    if role == UserRole.FARMER:
        return "farmer_dashboard.html"
    elif role == UserRole.LABOUR:
        return "labour_dashboard.html"
    elif role == UserRole.BUYER:
        return "buyer_dashboard.html"
    elif role == UserRole.ADMIN:
        return "admin_dashboard.html"
    return "index.html"



# ============================================================
# Firebase Token Verification Helper
# ============================================================

def verify_firebase_token(id_token):
    """
    Verify a Firebase ID token and return decoded claims.
    Returns dict with uid, phone_number, etc. or raises exception.
    """
    try:
        from firebase_admin import auth as firebase_auth

        decoded = firebase_auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        logger.warning("Firebase token verification failed: %s", e)
        raise InvalidFirebaseTokenError()


def _issue_auth_token(user):
    """Create or refresh an auth token for the user. Returns token string."""
    AuthToken.objects.filter(user=user).delete()
    token_value = generate_auth_token()
    AuthToken.objects.create(user=user, token=token_value)
    return token_value


# ============================================================
# Phone Registration (Farmer / Labour / Equipment Owner / Buyer)
# ============================================================

class PhoneRegistrationView(APIView):
    """
    POST /api/v1/accounts/register/phone/

    Register a new user via Firebase phone OTP.
    The client handles Firebase OTP flow and sends the resulting ID token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        decoded = verify_firebase_token(data["firebase_id_token"])

        firebase_uid = decoded.get("uid")
        phone = decoded.get("phone_number", "")

        if not phone:
            return error_response(
                "Phone number not found in Firebase token.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Check for duplicate registration
        if User.objects.filter(phone=phone).exists():
            raise UserAlreadyExistsError(
                "A user with this phone number already exists."
            )
        if User.objects.filter(firebase_uid=firebase_uid).exists():
            raise UserAlreadyExistsError(
                "This Firebase account is already registered."
            )

        # Create user
        user = User.objects.create_user(
            username=phone,
            phone=phone,
            country_code=data.get("country_code", "+91"),
            role=data["role"],
            firebase_uid=firebase_uid,
            name=data.get("name", ""),
            is_verified=True,  # Phone verified via Firebase
        )
        user.profile_completion_pct = calculate_profile_completion(user)
        user.save(update_fields=["profile_completion_pct"])

        token = _issue_auth_token(user)

        return success_response(
            data={
                "token": token,
                "user": UserProfileSerializer(user).data,
            },
            message="Registration successful.",
            status_code=status.HTTP_201_CREATED,
        )


# ============================================================
# Email Registration (Buyer)
# ============================================================

class EmailRegistrationView(APIView):
    """
    POST /api/v1/accounts/register/email/

    Register a buyer with email + password.
    Sends verification email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
            role=UserRole.BUYER,
            name=data["name"],
            phone=data.get("phone") or None,
            is_verified=False,
        )
        user.profile_completion_pct = calculate_profile_completion(user)
        user.save(update_fields=["profile_completion_pct"])

        # Send verification email
        self._send_verification_email(user)

        token = _issue_auth_token(user)

        return success_response(
            data={
                "token": token,
                "user": UserProfileSerializer(user).data,
            },
            message="Registration successful. Please verify your email.",
            status_code=status.HTTP_201_CREATED,
        )

    def _send_verification_email(self, user):
        """Generate verification token and send email."""
        token_value = generate_verification_token()
        EmailVerificationToken.objects.create(
            user=user,
            token=token_value,
            expires_at=timezone.now() + timedelta(hours=24),
        )

        verification_url = (
            f"{settings.ALLOWED_HOSTS[0]}/api/v1/accounts/verify-email/"
            f"?token={token_value}"
        )

        try:
            send_mail(
                subject="Agri Link — Verify Your Email",
                message=(
                    f"Hello {user.name},\n\n"
                    f"Please verify your email by visiting:\n{verification_url}\n\n"
                    f"This link expires in 24 hours.\n\n"
                    f"— Agri Link Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error("Failed to send verification email to %s: %s", user.email, e)


# ============================================================
# Email Verification
# ============================================================

class VerifyEmailView(APIView):
    """
    POST /api/v1/accounts/verify-email/

    Verify buyer email using the token sent via email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        token_value = request.data.get("token", "").strip()
        if not token_value:
            return error_response("Verification token is required.")

        try:
            token_obj = EmailVerificationToken.objects.get(
                token=token_value, is_used=False
            )
        except EmailVerificationToken.DoesNotExist:
            return error_response(
                "Invalid or already used verification token.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if token_obj.is_expired():
            return error_response(
                "Verification token has expired.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = token_obj.user
        user.is_verified = True
        user.save(update_fields=["is_verified"])
        token_obj.is_used = True
        token_obj.save(update_fields=["is_used"])

        return success_response(message="Email verified successfully.")


# ============================================================
# Phone Login
# ============================================================

class PhoneLoginView(APIView):
    """
    POST /api/v1/accounts/login/phone/

    Login via Firebase ID token (phone OTP).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        decoded = verify_firebase_token(serializer.validated_data["firebase_id_token"])
        firebase_uid = decoded.get("uid")

        try:
            user = User.objects.get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            raise UserNotFoundError(
                "No account found for this phone number. Please register first."
            )

        if not user.is_active:
            return error_response(
                "Your account is deactivated.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        token = _issue_auth_token(user)

        return success_response(
            data={
                "token": token,
                "user": UserProfileSerializer(user).data,
            },
            message="Login successful.",
        )


# ============================================================
# Dynamic Phone OTP Generation & Dispatch
# ============================================================

class SendOTPView(APIView):
    """
    POST /api/v1/accounts/otp/send/

    Generates a secure dynamic 6-digit OTP, stores it in database with expiry,
    and dispatches via SMS/Email.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        phone = data["phone"]
        role = data["role"]
        purpose = data.get("purpose", "login")

        user = User.objects.filter(phone=phone).first()
        if not user:
            user = User.objects.filter(phone=phone[-10:]).first()

        if purpose == "login":
            if user:
                if user.role != role:
                    return error_response(
                        f"This mobile number is registered as {user.role.capitalize()}, not {role.capitalize()}. Please sign in under {user.role.capitalize()} Login.",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                if not user.is_active:
                    return error_response(
                        "Your account has been deactivated. Please contact platform support.",
                        status_code=status.HTTP_403_FORBIDDEN,
                    )

        elif purpose == "register":
            if user:
                return error_response(
                    f"A user with mobile number {phone[-10:]} already exists. Please sign in instead.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        # Generate & send dynamic OTP
        dispatch_result = SMSService.send_otp(
            phone=phone,
            purpose=purpose,
            email=user.email if user else None,
        )

        resp_data = {
            "phone": phone,
            "expires_in": dispatch_result["expires_in"],
            "purpose": purpose,
        }
        if "dev_otp" in dispatch_result:
            resp_data["dev_otp"] = dispatch_result["dev_otp"]

        response_payload = {
            "success": True,
            "message": "Verification OTP has been dispatched to your mobile number.",
            "data": resp_data,
        }
        if "dev_otp" in dispatch_result:
            response_payload["dev_otp"] = dispatch_result["dev_otp"]

        return Response(response_payload, status=status.HTTP_200_OK)


# ============================================================
# Dynamic Phone OTP Verification & Login
# ============================================================

class VerifyOTPView(APIView):
    """
    POST /api/v1/accounts/otp/verify/

    Verifies dynamic OTP against database and issues 30-day session token.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        phone = data["phone"]
        otp = data["otp"]
        role = data["role"]

        valid, msg = SMSService.verify_otp(phone=phone, otp_code=otp, purpose="login")
        if not valid:
            return error_response(msg, status_code=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if not user:
            user = User.objects.filter(phone=phone[-10:]).first()

        if not user:
            clean_digits = phone.replace("+91", "").replace(" ", "").replace("-", "")
            user = User.objects.create_user(
                username=f"{role}_{clean_digits}",
                phone=f"+91{clean_digits}",
                role=role,
                name=f"{role.capitalize()} Partner",
                is_verified=True,
                is_active=True,
            )
        elif user.role != role:
            return error_response(
                f"Role mismatch: This user is registered as {user.role.capitalize()}, not {role.capitalize()}.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        if not user.is_active:
            return error_response(
                "Your account is inactive.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        if not user.is_verified:
            user.is_verified = True
            user.save(update_fields=["is_verified"])

        token = _issue_auth_token(user)
        redirect_url = get_dashboard_redirect(user.role)

        return success_response(
            data={
                "token": token,
                "user_id": user.id,
                "name": user.name,
                "role": user.role,
                "phone": user.phone,
                "user": UserProfileSerializer(user).data,
                "redirect_url": redirect_url,
            },
            message="Verification successful. Logged in.",
        )


# ============================================================
# Real User Registration (Farmer, Labour, Buyer)
# ============================================================

class UnifiedRegisterView(APIView):
    """
    POST /api/v1/accounts/register/

    Registers real user with PBKDF2 hashed password and validation.
    Admin registration via this endpoint is strictly blocked.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        name = data["name"].strip()
        phone = data["phone"]
        email = data.get("email") or None
        password = data["password"]
        role = data["role"]
        district = data.get("district", "").strip()
        state = data.get("state", "").strip()

        if role == UserRole.ADMIN:
            return error_response(
                "Admin accounts cannot be created via public registration.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # Generate unique username
        username = f"{role}_{phone[-10:]}"
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            phone=phone,
            email=email,
            password=password,  # Securely hashed via set_password
            role=role,
            name=name,
            district=district,
            state=state,
            is_verified=True,
            is_active=True,
        )
        user.profile_completion_pct = calculate_profile_completion(user)
        user.save(update_fields=["profile_completion_pct"])

        token = _issue_auth_token(user)
        redirect_url = get_dashboard_redirect(role)

        return success_response(
            data={
                "token": token,
                "user_id": user.id,
                "name": user.name,
                "role": user.role,
                "phone": user.phone,
                "user": UserProfileSerializer(user).data,
                "redirect_url": redirect_url,
            },
            message="Account registered successfully. Welcome to Agri Link!",
            status_code=status.HTTP_201_CREATED,
        )


# ============================================================
# Unified Login (Password or Phone OTP / Admin verification)
# ============================================================

class UnifiedLoginView(APIView):
    """
    POST /api/v1/accounts/login/

    Unified login supporting:
    1. Admin login with username/email/phone + password
    2. Phone + OTP login for any role
    3. Phone/email + password login for any role
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UnifiedLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        role = data["role"]
        identifier = (data.get("identifier") or data.get("username") or data.get("email") or data.get("phone") or "").strip()
        password = data.get("password")
        otp = data.get("otp")

        # Find user by phone, email, or username
        user = None
        clean_phone = identifier.replace(" ", "").replace("-", "")
        if clean_phone.startswith("+91"):
            user = User.objects.filter(phone=clean_phone).first()
        elif clean_phone.isdigit() and len(clean_phone) == 10:
            user = User.objects.filter(phone="+91" + clean_phone).first() or User.objects.filter(phone=clean_phone).first()

        if not user and "@" in identifier:
            user = User.objects.filter(email=identifier.lower()).first()

        if not user:
            user = User.objects.filter(username=identifier).first()

        if not user:
            return error_response(
                "Invalid credentials. No user found with the provided details.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Validate Role
        if user.role != role:
            return error_response(
                f"Role mismatch: This account is registered as {user.role.capitalize()}, not {role.capitalize()}.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # Admin specific verification
        if role == UserRole.ADMIN:
            if not (user.is_staff or user.is_superuser):
                return error_response(
                    "Access denied. Only authorized platform administrators may log in here.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
            if not password or not user.check_password(password):
                return error_response(
                    "Invalid admin password.",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            # Normal user (Farmer, Labour, Buyer)
            if otp:
                phone_to_check = user.phone or clean_phone
                valid, msg = SMSService.verify_otp(phone=phone_to_check, otp_code=otp, purpose="login")
                if not valid:
                    return error_response(msg, status_code=status.HTTP_400_BAD_REQUEST)
            elif password:
                if not user.check_password(password):
                    return error_response(
                        "Incorrect password.",
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                return error_response(
                    "Either password or OTP must be provided.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        if not user.is_active:
            return error_response(
                "Your account is inactive.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        token = _issue_auth_token(user)
        redirect_url = get_dashboard_redirect(user.role)

        if role == UserRole.ADMIN or user.is_staff:
            try:
                from django.contrib.auth import login as django_login
                django_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            except Exception as e:
                logger.warning("Session login for admin failed: %s", e)

        return success_response(
            data={
                "token": token,
                "user_id": user.id,
                "name": user.name,
                "role": user.role,
                "phone": user.phone,
                "user": UserProfileSerializer(user).data,
                "redirect_url": redirect_url,
            },
            message="Login successful.",
        )


# ============================================================
# Email Login (Buyer)
# ============================================================

class EmailLoginView(APIView):
    """
    POST /api/v1/accounts/login/email/

    Login with email + password (for buyers).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(email=data["email"].lower())
        except User.DoesNotExist:
            raise InvalidCredentialsError()

        if not user.check_password(data["password"]):
            raise InvalidCredentialsError()

        if not user.is_active:
            return error_response(
                "Your account is deactivated.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        if not user.is_verified:
            raise EmailNotVerifiedError()

        token = _issue_auth_token(user)

        return success_response(
            data={
                "token": token,
                "user": UserProfileSerializer(user).data,
            },
            message="Login successful.",
        )


# ============================================================
# Admin Login
# ============================================================

class AdminLoginView(APIView):
    """
    POST /admin-login/login/

    Admin login with username + password.
    Not visible on homepage.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(
                username=data["username"], role=UserRole.ADMIN
            )
        except User.DoesNotExist:
            raise InvalidCredentialsError()

        if not user.check_password(data["password"]):
            raise InvalidCredentialsError()

        token = _issue_auth_token(user)

        return success_response(
            data={
                "token": token,
                "user": UserProfileSerializer(user).data,
                "redirect_url": "admin_dashboard.html",
            },
            message="Admin login successful.",
        )


# ============================================================
# Profile
# ============================================================

class ProfileView(APIView):
    """
    GET  /api/v1/accounts/profile/     — Get own profile
    PUT  /api/v1/accounts/profile/     — Update own profile
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return success_response(data=serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Recalculate profile completion
        request.user.profile_completion_pct = calculate_profile_completion(
            request.user
        )
        request.user.save(update_fields=["profile_completion_pct"])

        return success_response(
            data=UserProfileSerializer(request.user).data,
            message="Profile updated.",
        )


# ============================================================
# Profile Photo Upload
# ============================================================

class ProfilePhotoView(APIView):
    """
    POST /api/v1/accounts/profile/photo/

    Upload profile photo to Cloudinary.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfilePhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        photo = serializer.validated_data["photo"]
        url = upload_to_cloudinary(photo, folder="agrilink/profiles")

        request.user.profile_photo_url = url
        request.user.profile_completion_pct = calculate_profile_completion(
            request.user
        )
        request.user.save(update_fields=["profile_photo_url", "profile_completion_pct"])

        return success_response(
            data={"profile_photo_url": url},
            message="Profile photo uploaded.",
        )


# ============================================================
# Forgot Password
# ============================================================

class ForgotPasswordView(APIView):
    """
    POST /api/v1/accounts/forgot-password/

    Send password reset link to buyer's email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower()

        try:
            user = User.objects.get(email=email, role=UserRole.BUYER)
        except User.DoesNotExist:
            # Don't reveal whether email exists
            return success_response(
                message="If an account exists with this email, a reset link has been sent."
            )

        # Invalidate old tokens
        PasswordResetToken.objects.filter(user=user, is_used=False).update(
            is_used=True
        )

        token_value = generate_verification_token()
        PasswordResetToken.objects.create(
            user=user,
            token=token_value,
            expires_at=timezone.now() + timedelta(hours=1),
        )

        try:
            send_mail(
                subject="Agri Link — Reset Your Password",
                message=(
                    f"Hello {user.name},\n\n"
                    f"Use this token to reset your password:\n{token_value}\n\n"
                    f"This token expires in 1 hour.\n\n"
                    f"— Agri Link Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error("Failed to send reset email to %s: %s", email, e)

        return success_response(
            message="If an account exists with this email, a reset link has been sent."
        )


# ============================================================
# Reset Password
# ============================================================

class ResetPasswordView(APIView):
    """
    POST /api/v1/accounts/reset-password/

    Reset password using the token from email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            token_obj = PasswordResetToken.objects.get(
                token=data["token"], is_used=False
            )
        except PasswordResetToken.DoesNotExist:
            return error_response(
                "Invalid or expired reset token.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if token_obj.is_expired():
            return error_response(
                "Reset token has expired.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = token_obj.user
        user.set_password(data["new_password"])
        user.save(update_fields=["password"])

        token_obj.is_used = True
        token_obj.save(update_fields=["is_used"])

        # Invalidate existing auth tokens
        AuthToken.objects.filter(user=user).delete()

        return success_response(message="Password reset successful. Please login again.")


# ============================================================
# Logout
# ============================================================

class LogoutView(APIView):
    """
    POST /api/v1/accounts/logout/

    Invalidate the user's auth token and clear any session state.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user and request.user.is_authenticated:
            AuthToken.objects.filter(user=request.user).delete()

        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Token "):
            raw_token = auth_header.split(" ", 1)[1].strip()
            AuthToken.objects.filter(token=raw_token).delete()

        django_logout(request)
        return success_response(message="Logged out successfully.")


# ============================================================
# Change Password
# ============================================================

class ChangePasswordView(APIView):
    """
    POST /api/v1/accounts/change-password/

    Change password for the currently authenticated user.
    Requires: old_password, new_password, confirm_password
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get("old_password", "").strip()
        new_password = request.data.get("new_password", "").strip()
        confirm_password = request.data.get("confirm_password", "").strip()

        if not old_password or not new_password or not confirm_password:
            return error_response(
                "old_password, new_password, and confirm_password are required.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.check_password(old_password):
            return error_response(
                "Current password is incorrect.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if new_password != confirm_password:
            return error_response(
                "New passwords do not match.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if len(new_password) < 8:
            return error_response(
                "New password must be at least 8 characters.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.save(update_fields=["password"])

        # Invalidate existing auth tokens and issue a new one
        AuthToken.objects.filter(user=request.user).delete()
        new_token = _issue_auth_token(request.user)

        return success_response(
            data={"token": new_token},
            message="Password changed successfully. Please use the new token.",
        )
