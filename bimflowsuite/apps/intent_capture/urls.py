from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IntentCaptureViewSet, ProgramSpecViewSet  # FIXED: Import ViewSets

router = DefaultRouter()
router.register(r'intents', IntentCaptureViewSet)  # FIXED: ViewSet for CRUD
router.register(r'specs', ProgramSpecViewSet)

urlpatterns = [
    path('', include(router.urls)),
]