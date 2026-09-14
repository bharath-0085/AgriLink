from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_accounts(apps, schema_editor):
    User = apps.get_model("accounts", "User")

    # 1. Guarantee Platform Administrator superuser exists and is active
    admin_user = User.objects.filter(username="admin").first()
    if not admin_user:
        User.objects.create(
            username="admin",
            email="admin@agrilink.in",
            password=make_password("AdminMaster@2026"),
            role="admin",
            name="Platform Administrator",
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )
    else:
        admin_user.role = "admin"
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.is_verified = True
        admin_user.password = make_password("AdminMaster@2026")
        admin_user.save()

    # 2. Guarantee Verified Produce Buyer exists and is active
    buyer_user = User.objects.filter(email__iexact="buyer@agrilink.in").first()
    if not buyer_user:
        buyer_user = User.objects.filter(role="buyer").first()

    if not buyer_user:
        User.objects.create(
            username="buyer_9842199884",
            email="buyer@agrilink.in",
            phone="+919842199884",
            password=make_password("Buyer@2026"),
            role="buyer",
            name="Aditi Sharma (Buyer)",
            district="Chennai",
            state="Tamil Nadu",
            is_active=True,
            is_verified=True,
        )
    else:
        buyer_user.email = "buyer@agrilink.in"
        buyer_user.role = "buyer"
        buyer_user.is_active = True
        buyer_user.is_verified = True
        buyer_user.password = make_password("Buyer@2026")
        if not buyer_user.phone:
            buyer_user.phone = "+919842199884"
        buyer_user.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_phoneotp"),
    ]

    operations = [
        migrations.RunPython(seed_accounts, reverse_func),
    ]
