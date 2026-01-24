from django.apps import AppConfig

class ComplianceEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.compliance_engine'

    def ready(self):
        pass