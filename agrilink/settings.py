"""
Agri Link — Django Settings
============================
Production-ready configuration for the Agri Link agriculture platform.
"""

import os
from pathlib import Path
from decouple import config, Csv

# ============================================================
# BASE DIRECTORY
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SECURITY
# ============================================================
SECRET_KEY = config("SECRET_KEY", default=config("DJANGO_SECRET_KEY", default="django-insecure-change-me-in-production"))
DEBUG = config("DEBUG", default=config("DJANGO_DEBUG", default=False, cast=bool), cast=bool)
_raw_hosts = config("DJANGO_ALLOWED_HOSTS", default=config("ALLOWED_HOSTS", default="*"))
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()] if isinstance(_raw_hosts, str) else list(_raw_hosts)
for _h in ["localhost", "127.0.0.1", ".onrender.com"]:
    if _h not in ALLOWED_HOSTS and "*" not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_h)
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS and "*" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="http://localhost:8000,http://127.0.0.1:8000,https://*.onrender.com",
    cast=Csv(),
)
if RENDER_EXTERNAL_HOSTNAME:
    _render_origin = f"https://{RENDER_EXTERNAL_HOSTNAME}"
    if _render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_render_origin)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ============================================================
# DUAL DATABASE CONFIGURATION (SQLite / MongoDB Atlas)
# ============================================================
USE_SQLITE = config("USE_SQLITE", default=True, cast=bool)

if USE_SQLITE:
    INSTALLED_APPS = [
        # Django built-in (Standard for SQLite)
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # Third-party
        "rest_framework",
        "corsheaders",
        # Project apps
        "apps.core",
        "apps.accounts",
        "apps.farmer",
        "apps.buyer",
        "apps.labour",
        "apps.equipment",
        "apps.marketplace",
        "apps.weather",
        "apps.chat",
        "apps.notification",
        "apps.ai_module",
        "apps.adminpanel",
    ]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
else:
    INSTALLED_APPS = [
        # Django built-in (overridden for MongoDB compatibility)
        "apps.core.mongodb_configs.MongoAdminConfig",
        "apps.core.mongodb_configs.MongoAuthConfig",
        "apps.core.mongodb_configs.MongoContentTypesConfig",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # Third-party
        "rest_framework",
        "corsheaders",
        # Project apps
        "apps.core",
        "apps.accounts",
        "apps.farmer",
        "apps.buyer",
        "apps.labour",
        "apps.equipment",
        "apps.marketplace",
        "apps.weather",
        "apps.chat",
        "apps.notification",
        "apps.ai_module",
        "apps.adminpanel",
    ]
    DATABASES = {
        "default": {
            "ENGINE": "django_mongodb_backend",
            "HOST": config("MONGO_URI", default=config("MONGODB_URI", default="mongodb://localhost:27017")),
            "NAME": config("MONGODB_NAME", default="agrilink_db"),
        },
    }
    DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"

# ============================================================
# MIDDLEWARE
# ============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "agrilink.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "agrilink.wsgi.application"

# ============================================================
# CUSTOM USER MODEL
# ============================================================
AUTH_USER_MODEL = "accounts.User"

# ============================================================
# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ============================================================
# INTERNATIONALIZATION
# ============================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ============================================================
# STATIC FILES
# ============================================================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# ============================================================
# MEDIA FILES
# ============================================================
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================================================
# REST FRAMEWORK
# ============================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.core.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "apps.core.utils.StandardPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/minute",
        "user": "120/minute",
    },
}

# ============================================================
# CORS
# ============================================================
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000,http://127.0.0.1:8000",
    cast=Csv(),
)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https:\/\/.*\.onrender\.com$",
]


# ============================================================
# CLOUDINARY
# ============================================================
CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_NAME", default=config("CLOUDINARY_CLOUD_NAME", default=""))
CLOUDINARY_API_KEY = config("CLOUDINARY_KEY", default=config("CLOUDINARY_API_KEY", default=""))
CLOUDINARY_API_SECRET = config("CLOUDINARY_SECRET", default=config("CLOUDINARY_API_SECRET", default=""))

# ============================================================
# FIREBASE
# ============================================================
FIREBASE_SERVICE_ACCOUNT_PATH = config(
    "FIREBASE_CREDENTIALS",
    default=config(
        "FIREBASE_SERVICE_ACCOUNT_PATH",
        default=str(BASE_DIR / "firebase-service-account.json")
    ),
)

# ============================================================
# OPENWEATHER API
# ============================================================
OPENWEATHER_API_KEY = config("OPENWEATHER_API_KEY", default=config("WEATHER_API_KEY", default=""))

# ============================================================
# GOOGLE GEMINI API
# ============================================================
GEMINI_API_KEY = config("GEMINI_API_KEY", default="")

# ============================================================
# EMAIL — Gmail SMTP
# ============================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@agrilink.com")

# ============================================================
# AI MODEL PATHS
# ============================================================
AI_CROP_RECOMMENDATION_DIR = BASE_DIR / "AI" / "crop_recommendation"
AI_DISEASE_DETECTION_DIR = BASE_DIR / "AI" / "disease_detection"

# ============================================================
# WEATHER CACHE TTL (seconds)
# ============================================================
WEATHER_CACHE_TTL = 1800  # 30 minutes

# ============================================================
# OTP SETTINGS
# ============================================================
OTP_EXPIRY_SECONDS = 300  # 5 minutes
OTP_RESEND_COOLDOWN_SECONDS = 30
OTP_MAX_RETRIES = 5
ENABLE_DEV_OTP = config("ENABLE_DEV_OTP", default=True, cast=bool)

# ============================================================
# FIREBASE INITIALIZATION
# ============================================================
import firebase_admin
from firebase_admin import credentials as firebase_credentials

_firebase_cred_path = FIREBASE_SERVICE_ACCOUNT_PATH
if os.path.exists(_firebase_cred_path) and not firebase_admin._apps:
    _cred = firebase_credentials.Certificate(_firebase_cred_path)
    firebase_admin.initialize_app(_cred)

# ============================================================
# CLOUDINARY INITIALIZATION
# ============================================================
if CLOUDINARY_CLOUD_NAME:
    import cloudinary
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True,
    )

# ============================================================
# LOGGING
# ============================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
}
