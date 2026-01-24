from .common import *  # noqa: F403


DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

PASSWORD = os.environ.get("POSTGRES_PASSWORD")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY": "error",
    "EXCEPTION_HANDLER": "bimflow.utils.handle_exceptions.custom_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ("http://localhost:8081", "http://localhost:4200")

CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1", "http://localhost:4200"]

# For sending email
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = True
