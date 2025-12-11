from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect, render  # FIXED: render for form
from django.views import View
from django.http import HttpResponseRedirect  # FIXED: For POST forward

# REST Framework & JWT
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# GraphQL
from graphene_django.views import GraphQLView
from bimflow.schema import schema

# Swagger / ReDoc Documentation
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator  # FIXED: Direct import (no swagger_settings)

# -------------------------------------------------
# 🔹 Dummy Login View (fixes Swagger redirect – Renders POST form)
# -------------------------------------------------
class DummyLoginView(View):
    def get(self, request):
        next_url = request.GET.get('next', '/swagger/')
        return render(request, 'login.html', {'next': next_url})  # Renders form

    def post(self, request):
        # Forward POST to /api/token/ (no 405)
        from django.http import HttpResponse
        import requests
        response = requests.post('http://127.0.0.1:8000/api/token/', json=request.POST)
        if response.status_code == 200:
            return HttpResponse(response.content, status=200)
        return HttpResponse(response.content, status=response.status_code)

# -------------------------------------------------
# 🔹 API Documentation (Swagger + ReDoc)
# -------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="BIMFlow Suite API",
        default_version='v1',
        description="Open-source BIM automation. Auth: Use /v1/auth/login/ in Swagger (editable form for username/password) → Get token → Paste 'Bearer <access>' in Authorize.",
        contact=openapi.Contact(email="support@bimflow.dev"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=OpenAPISchemaGenerator,  # FIXED: Direct class (no AttributeError)
)

# -------------------------------------------------
# 🔹 URL Patterns
# -------------------------------------------------
urlpatterns = [
    # Root redirect to Swagger
    path('', lambda request: redirect('swagger-ui'), name='home-redirect'),

    # FIXED: Dummy /accounts/login/ (renders POST form to token – no 405)
    path('accounts/login/', DummyLoginView.as_view(), name='dummy-login'),

    # Django Admin
    path('admin/', admin.site.urls),

    # API Routes
    path('api/v1/', include('api.v1.urls')),

    # REST Framework built-in
    path('api-auth/', include('rest_framework.urls')),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # GraphQL
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),

    # Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
]

# Static & Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)