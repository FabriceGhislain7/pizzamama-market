"""
Base settings.
"""

import os
from pathlib import Path
from datetime import timedelta
import dj_database_url


# Base dir
BASE_DIR = Path(__file__).resolve().parents[2]


# Security
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-dev-key")

DEBUG = False

ALLOWED_HOSTS = []


# Applications
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",

    # Local
    "apps.accounts",
    "apps.products",
    "apps.orders",
]


# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# JWT (JSON Web Token) Configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# URLs
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default PK
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Custom user
AUTH_USER_MODEL = "accounts.User"


# DRF Configuration
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",
}


# OpenAPI / Schema
SPECTACULAR_SETTINGS = {
    "TITLE": "PizzaMama API",
    "VERSION": "1.0.0",
}