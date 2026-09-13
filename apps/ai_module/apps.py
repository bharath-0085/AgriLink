from django.apps import AppConfig


class AiModuleConfig(AppConfig):
    from decouple import config
    default_auto_field = "django.db.models.BigAutoField" if config("USE_SQLITE", default=True, cast=bool) else "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "apps.ai_module"
    verbose_name = "AI Module"
