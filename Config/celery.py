import os
from celery import Celery
from django.conf import settings
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ["DJANGO_SETTINGS_MODULE"])
 
app = Celery("Config")
# CLELERY - all Celery-related configuration keys
app.config_from_object(settings, namespace='CELERY')
# Load task modules from all registered Django app config
app.autodiscover_tasks()

