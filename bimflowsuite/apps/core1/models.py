from django.db import models

class ScenarioVersion(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} v{self.version}"