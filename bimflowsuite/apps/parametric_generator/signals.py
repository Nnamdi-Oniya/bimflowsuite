from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import GeneratedIFC

@receiver(post_migrate, sender='parametric_generator')
def load_default_assets(sender, **kwargs):
    GeneratedIFC