"""
Agri Link — SMS & OTP Dispatch Service
=======================================
Multi-channel notification service for dynamic phone OTP and email delivery.
Cleanly extensible for SMS providers (Twilio, Fast2SMS, MSG91, etc.) via .env.
"""

import logging
import secrets
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from decouple import config

from apps.accounts.models import PhoneOTP

logger = logging.getLogger(__name__)


def generate_secure_otp(length=6) -> str:
    """
    Generate a cryptographically secure numeric OTP of given length.
    Never returns a fixed or predictable code.
    """
    min_val = 10 ** (length - 1)
    max_val = (10 ** length) - 1
    return str(secrets.randbelow(max_val - min_val + 1) + min_val)


class SMSService:
    """
    Pluggable SMS & OTP Dispatcher.
    If third-party SMS credentials (Twilio, Fast2SMS) are provided in .env,
    it delivers SMS via the external provider.
    Also supports sending OTP via configured Gmail SMTP email.
    """

    @classmethod
    def send_otp(cls, phone: str, purpose: str = "login", email: str = None) -> dict:
        """
        Generate dynamic OTP, persist to database with expiry, and dispatch.
        """
        # Normalize phone
        clean_phone = phone.strip().replace(" ", "").replace("-", "")
        if not clean_phone.startswith("+91") and len(clean_phone) == 10:
            clean_phone = "+91" + clean_phone

        # Invalidate any existing unused OTPs for this phone and purpose
        PhoneOTP.objects.filter(phone=clean_phone, purpose=purpose, is_used=False).update(is_used=True)

        # Generate fresh dynamic 6-digit OTP
        otp_code = generate_secure_otp(6)
        expiry_seconds = getattr(settings, "OTP_EXPIRY_SECONDS", 300)
        expires_at = timezone.now() + timedelta(seconds=expiry_seconds)

        # Save to database
        otp_record = PhoneOTP.objects.create(
            phone=clean_phone,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at,
            is_used=False,
            attempts=0,
        )

        # Dispatch through external SMS provider if configured
        sms_sent = cls._dispatch_sms(clean_phone, otp_code, purpose)

        # Also dispatch to Email if email address is available
        email_sent = False
        if email:
            email_sent = cls._dispatch_email(email, otp_code, purpose)

        logger.info(
            "Dynamic OTP generated for %s (purpose: %s, expires_in: %ds). SMS sent: %s, Email sent: %s",
            clean_phone,
            purpose,
            expiry_seconds,
            sms_sent,
            email_sent,
        )

        result = {
            "success": True,
            "phone": clean_phone,
            "purpose": purpose,
            "expires_in": expiry_seconds,
            "sms_sent": sms_sent,
            "email_sent": email_sent,
        }

        # In DEBUG / development mode, provide dev_otp so testing is seamless without third-party SMS bills
        if getattr(settings, "DEBUG", False):
            result["dev_otp"] = otp_code

        return result

    @classmethod
    def verify_otp(cls, phone: str, otp_code: str, purpose: str = "login") -> tuple[bool, str]:
        """
        Verify the provided OTP against the database record.
        Enforces single-use, expiration, and attempt limits.
        """
        clean_phone = phone.strip().replace(" ", "").replace("-", "")
        if not clean_phone.startswith("+91") and len(clean_phone) == 10:
            clean_phone = "+91" + clean_phone

        otp_record = PhoneOTP.objects.filter(
            phone=clean_phone,
            purpose=purpose,
            is_used=False,
        ).order_by("-created_at").first()

        if not otp_record:
            return False, "No active OTP found. Please request a new verification code."

        valid, msg = otp_record.is_valid(otp_code)
        if not valid:
            return False, msg

        # Mark OTP as used to prevent replay
        otp_record.is_used = True
        otp_record.save(update_fields=["is_used"])
        return True, "Verification successful."

    @classmethod
    def _dispatch_sms(cls, phone: str, otp_code: str, purpose: str) -> bool:
        """
        Dispatch SMS using configured provider in .env.
        Supports Twilio, Fast2SMS, etc.
        """
        provider = config("SMS_PROVIDER", default="").lower()

        if provider == "twilio":
            try:
                account_sid = config("TWILIO_ACCOUNT_SID", default="")
                auth_token = config("TWILIO_AUTH_TOKEN", default="")
                from_number = config("TWILIO_PHONE_NUMBER", default="")
                if account_sid and auth_token and from_number:
                    from twilio.rest import Client
                    client = Client(account_sid, auth_token)
                    client.messages.create(
                        body=f"Your Agri Link verification code is: {otp_code}. Valid for 5 minutes. Do not share this code.",
                        from_=from_number,
                        to=phone,
                    )
                    return True
            except Exception as e:
                logger.error("Twilio SMS dispatch failed: %s", e)
                return False

        elif provider == "fast2sms":
            try:
                import urllib.request
                import json
                api_key = config("FAST2SMS_API_KEY", default="")
                if api_key:
                    # Strip +91 for Fast2SMS numbers
                    local_num = phone[-10:]
                    url = "https://www.fast2sms.com/dev/bulkV2"
                    payload = json.dumps({
                        "route": "otp",
                        "variables_values": otp_code,
                        "numbers": local_num,
                    }).encode("utf-8")
                    req = urllib.request.Request(url, data=payload, headers={
                        "authorization": api_key,
                        "Content-Type": "application/json"
                    })
                    with urllib.request.urlopen(req) as resp:
                        try:
                            resp_json = json.loads(resp.read().decode())
                            if resp_json.get("return") is True:
                                return True
                            logger.warning("Fast2SMS dispatch returned: %s", resp_json.get("message"))
                            return False
                        except Exception:
                            return resp.status == 200
            except Exception as e:
                logger.error("Fast2SMS dispatch failed: %s", e)
                return False

        # If no external provider configured, gracefully log
        logger.info("[SMS GATEWAY NOTICE] No SMS_PROVIDER active in .env. Set TWILIO or FAST2SMS to send live carrier SMS.")
        return False

    @classmethod
    def _dispatch_email(cls, email: str, otp_code: str, purpose: str) -> bool:
        """
        Send verification OTP code via Gmail SMTP if configured.
        """
        try:
            subject = "Agri Link — Your Verification OTP Code"
            message = (
                f"Hello,\n\n"
                f"Your Agri Link verification code for {purpose} is: {otp_code}\n\n"
                f"This code will expire in 5 minutes.\n"
                f"If you did not request this, please ignore this message.\n\n"
                f"— Agri Link Security Team"
            )
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@agrilink.com")
            send_mail(subject, message, from_email, [email], fail_silently=True)
            return True
        except Exception as e:
            logger.error("Email OTP dispatch failed to %s: %s", email, e)
            return False
