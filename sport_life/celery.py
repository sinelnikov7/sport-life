import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sport_life.settings')
app = Celery('sport_life')
app.config_from_object('django.conf:settings', namespace='CELERY')
