import logging
from django.apps import AppConfig
from django.db.models.signals import post_migrate

logger = logging.getLogger(__name__)


def ensure_core_accounts(sender=None, **kwargs):
    """
    Ensure the production administrator and demo produce buyer accounts
    exist, are active, and have the appropriate privileges and passwords.
    """
    try:
        from django.contrib.auth import get_user_model
        from apps.core.constants import UserRole

        User = get_user_model()

        # 1. Platform Administrator
        admin_user = User.objects.filter(username="admin").first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username="admin",
                password="AdminMaster@2026",
                email="admin@agrilink.in",
                role=UserRole.ADMIN,
                name="Platform Administrator",
                is_staff=True,
                is_superuser=True,
                is_active=True,
                is_verified=True,
            )
            logger.info("Created default platform administrator account.")
        else:
            changed = False
            if admin_user.role != UserRole.ADMIN:
                admin_user.role = UserRole.ADMIN
                changed = True
            if not admin_user.is_staff:
                admin_user.is_staff = True
                changed = True
            if not admin_user.is_superuser:
                admin_user.is_superuser = True
                changed = True
            if not admin_user.is_active:
                admin_user.is_active = True
                changed = True
            if not admin_user.is_verified:
                admin_user.is_verified = True
                changed = True
            if not admin_user.check_password("AdminMaster@2026"):
                admin_user.set_password("AdminMaster@2026")
                changed = True
            if changed:
                admin_user.save()
                logger.info("Updated platform administrator permissions and status.")

        # 2. Verified Produce Buyer
        buyer_user = User.objects.filter(email__iexact="buyer@agrilink.in").first()
        if not buyer_user:
            buyer_user = User.objects.filter(role=UserRole.BUYER).first()

        if not buyer_user:
            buyer_user = User.objects.create_user(
                username="buyer_9842199884",
                email="buyer@agrilink.in",
                phone="+919842199884",
                role=UserRole.BUYER,
                name="Aditi Sharma (Buyer)",
                district="Chennai",
                state="Tamil Nadu",
                is_active=True,
                is_verified=True,
            )
            buyer_user.set_password("Buyer@2026")
            buyer_user.save()
            logger.info("Created default verified produce buyer account.")
        else:
            changed = False
            if buyer_user.email != "buyer@agrilink.in":
                buyer_user.email = "buyer@agrilink.in"
                changed = True
            if buyer_user.role != UserRole.BUYER:
                buyer_user.role = UserRole.BUYER
                changed = True
            if not buyer_user.is_active:
                buyer_user.is_active = True
                changed = True
            if not buyer_user.is_verified:
                buyer_user.is_verified = True
                changed = True
            if not buyer_user.check_password("Buyer@2026"):
                buyer_user.set_password("Buyer@2026")
                changed = True
            if not buyer_user.phone:
                buyer_user.phone = "+919842199884"
                changed = True
            if changed:
                buyer_user.save()
                logger.info("Updated verified produce buyer account status.")

    except Exception as e:
        logger.debug("Database not yet initialized for account seeding: %s", e)


class AccountsConfig(AppConfig):
    from decouple import config
    default_auto_field = "django.db.models.BigAutoField" if config("USE_SQLITE", default=True, cast=bool) else "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.accounts"
    verbose_name = "Accounts"

    def ready(self):
        post_migrate.connect(ensure_core_accounts, sender=self)
