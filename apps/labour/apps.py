from django.apps import AppConfig


class LabourConfig(AppConfig):
    from decouple import config
    default_auto_field = "django.db.models.BigAutoField" if config("USE_SQLITE", default=True, cast=bool) else "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.labour"
    verbose_name = "Labour"
