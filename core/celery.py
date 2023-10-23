import os
from celery import Celery
from datetime import timedelta
from core import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
 
app.conf.timezone = settings.TIME_ZONE
 
app.conf.beat_schedule = {
    "sync_forecast_data": {
        "task": "api.tasks.sync_forecast_data",
        "schedule": timedelta(minutes=30),
    },
}

app.autodiscover_tasks()