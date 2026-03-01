from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# REST Framework & JWT
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.users.views import EmailOrUsernameTokenObtainPairView

# GraphQL
from graphene_django.views import GraphQLView
import schema

# OpenAPI / Swagger / ReDoc Documentation (drf-spectacular)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Customize admin site
admin.site.site_header = "BIMFlow Suite Admin"
admin.site.site_title = "BIMFlow Suite"
admin.site.index_title = "Welcome to BIMFlow Suite Administration"


# -------------------------------------------------
# 🔹 URL Patterns
# -------------------------------------------------
urlpatterns = [
    # Root redirect to Swagger documentation
    path("", lambda request: redirect("swagger-ui"), name="home-redirect"),
    # Django Admin
    path("admin/bimflow/", admin.site.urls),
    # API Routes (v1)
    path("api/v1/", include("apps.users.urls")),
    # REST Framework built-in (for browsable API)
    path("api-auth/", include("rest_framework.urls")),
    # JWT Authentication endpoints
    path(
        "api/token/",
        EmailOrUsernameTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        extend_schema_view(
            post=extend_schema(
                tags=["token"],
                description="Refresh JWT access token using a valid refresh token.",
            )
        )(TokenRefreshView).as_view(),
        name="token_refresh",
    ),
    # GraphQL endpoint
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # API Documentation
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc-ui"),
]

# Static & Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
