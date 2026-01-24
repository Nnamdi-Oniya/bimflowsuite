from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Customize admin site
admin.site.site_header = "BIMFlow Suite Admin"
admin.site.site_title = "BIMFlow Suite"
admin.site.index_title = "Welcome to BIMFlow Suite Administration"

# REST Framework & JWT
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# GraphQL
from graphene_django.views import GraphQLView
from bimflow import schema

# Swagger / ReDoc Documentation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


# -------------------------------------------------
# 🔹 API Documentation (Swagger + ReDoc)
# -------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="BIMFlow Suite API",
        default_version="v1",
        description="Open-source BIM automation toolkit. Authenticate via /api/v1/auth/login/ to get JWT token, then use Authorize button in Swagger to test endpoints.",
        contact=openapi.Contact(email="support@bimflow.dev"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=OpenAPISchemaGenerator,
)

# -------------------------------------------------
# 🔹 URL Patterns
# -------------------------------------------------
urlpatterns = [
    # Root redirect to Swagger documentation
    path("", lambda request: redirect("swagger-ui"), name="home-redirect"),
    # Django Admin
    path("admin/", admin.site.urls),
    # API Routes (v1)
    path("api/v1/", include("apps.users.urls")),
    # REST Framework built-in (for browsable API)
    path("api-auth/", include("rest_framework.urls")),
    # JWT Authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # GraphQL endpoint
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
    # API Documentation
    path(
        "swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
]

# Static & Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
