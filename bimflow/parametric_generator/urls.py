from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parametric_generator import views  # Import ViewSet

router = DefaultRouter()
router.register(r'generate/models', views.GeneratedModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Explicit for clarity (optional)
    path('generate/models/generate/', views.GeneratedModelViewSet.as_view({'post': 'generate'})),
]