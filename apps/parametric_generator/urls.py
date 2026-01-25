from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, GeneratedIFCViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"ifcs", GeneratedIFCViewSet, basename="generated-ifc")

app_name = "bim_projects"

urlpatterns = [
    path("", include(router.urls)),
]
