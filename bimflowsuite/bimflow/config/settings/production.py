from .common import *  # noqa: F403

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", '127.0.0.1').split(",")  # noqa: F405

DEBUG = False

EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")  # noqa: F405

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
      # noqa: F405
]

SECURE_HSTS_SECONDS = 5 * 60
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

X_FRAME_OPTIONS = 'DENY'

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

DATABASE_USER = os.environ.get("DATABASE_USER")

PASSWORD = os.environ.get("DATABASE_PASSWORD")

DATABASE_NAME = os.environ.get("DATABASE_NAME")

DATABASE_PORT = os.environ.get("DATABASE_PORT")

DATABASE_HOST = os.environ.get("DATABASE_HOST")

CORS_ORIGIN_WHITELIST = (
    'https://www.bimflowsuite.com', 'https://bimflowsuite.com', 'http://localhost:4200', 'https://dev.bimflowsuite.com'
)


REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'error',
    'EXCEPTION_HANDLER': 'bimflow.utils.handle_exceptions.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/minute',
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'SEARCH_PARAM': 'filter[search]',
}

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = True
