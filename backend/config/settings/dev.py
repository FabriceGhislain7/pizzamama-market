from .base import *
from dotenv import load_dotenv

# Carica variabili ambiente solo in sviluppo
load_dotenv(BASE_DIR / ".env")

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

MEDIA_ROOT = BASE_DIR / "media"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# In sviluppo permettiamo anche SessionAuthentication
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += [
    "rest_framework.authentication.SessionAuthentication",
]