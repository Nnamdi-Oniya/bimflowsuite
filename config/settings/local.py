from .common import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname}: {asctime} {process:d}:{thread:d} {name} - {message}",
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
        "level": "DEBUG",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

_allowed_origins = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
)
CORS_ALLOWED_ORIGINS = _allowed_origins.split(",") if _allowed_origins else []

CORS_ALLOW_CREDENTIALS = (
    os.environ.get("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
)

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Local async fallback: allow running without Redis.
# Set USE_REDIS=true to use real Redis/Celery/Channels behavior in local.
USE_REDIS = os.getenv("USE_REDIS", "false").lower() == "true"

if not USE_REDIS:
    # Ensure Celery does not read Redis URLs from .env in local fallback mode.
    os.environ["CELERY_BROKER_URL"] = "memory://"
    os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"
    os.environ["BROKER_URL"] = "memory://"
    os.environ["RESULT_BACKEND"] = "cache+memory://"

    # Run Celery tasks in-process (synchronous) for local development.
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_TASK_STORE_EAGER_RESULT = False
    CELERY_IGNORE_RESULT = True
    CELERY_BROKER_URL = "memory://"
    CELERY_RESULT_BACKEND = "cache+memory://"

    # Use in-memory channel layer instead of Redis.
    CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
    }
