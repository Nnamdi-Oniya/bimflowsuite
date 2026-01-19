from django.urls import path, include
from .auth.views import LoginView, RegisterView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('intent/', include('apps.intent_capture.urls')),
    path('generate/', include('apps.parametric_generator.urls')),  # Single 'generate/'
    path('compliance/', include('apps.compliance_engine.urls')),
    path('analytics/', include('apps.analytics.urls')),
    # path('scenarios/', include('bimflow.core.scenario_manager.urls')),  # Future: Uncomment after full core app
]