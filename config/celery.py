import os

from celery import Celery
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("bimflowsuite")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.conf.task_always_eager = getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False)
app.conf.task_eager_propagates = getattr(
    settings, "CELERY_TASK_EAGER_PROPAGATES", False
)
app.conf.task_store_eager_result = getattr(
    settings, "CELERY_TASK_STORE_EAGER_RESULT", False
)
app.conf.task_ignore_result = getattr(settings, "CELERY_IGNORE_RESULT", False)
app.autodiscover_tasks()
