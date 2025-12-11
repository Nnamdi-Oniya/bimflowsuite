from django.apps import AppConfig

class ParametricGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parametric_generator'

    def ready(self):
        import parametric_generator.signals  # noqa: F401 (loads post-migrate signal)