from django.db import models
from ....core.models import ScenarioVersion  # Import from core

# Stub for scenario manager (future)
class Scenario(models.Model):
    """
    Stub for scenario (links to versions).
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    version = models.ForeignKey(ScenarioVersion, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Scenario"
        verbose_name_plural = "Scenarios"

    def __str__(self):
        return self.name