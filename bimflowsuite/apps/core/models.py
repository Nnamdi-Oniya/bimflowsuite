from django.db import models

# Stub for future core models (e.g., ScenarioVersion)
class ScenarioVersion(models.Model):
    """
    Stub model for scenario versioning (add details later).
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Scenario Version"
        verbose_name_plural = "Scenario Versions"

    def __str__(self):
        return self.name