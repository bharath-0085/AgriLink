from django.apps import AppConfig


class NotificationConfig(AppConfig):
    from decouple import config
    default_auto_field = "django.db.models.BigAutoField" if config("USE_SQLITE", default=True, cast=bool) else "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.notification"
    verbose_name = "Notification"
