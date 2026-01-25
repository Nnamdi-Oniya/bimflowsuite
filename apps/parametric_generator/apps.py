from django.apps import AppConfig

class ParametricGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.parametric_generator'

    def ready(self):
        import apps.parametric_generator.signals  # noqa: F401 (loads post-migrate signal)