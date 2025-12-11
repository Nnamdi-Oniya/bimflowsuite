from django.apps import AppConfig

class IntentCaptureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'intent_capture'

    def ready(self):
        pass