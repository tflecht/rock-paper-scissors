import os

from celery import Celery
from celery.signals import setup_logging


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_server.settings")
app = Celery("web_server")
app.config_from_object("django.conf:settings", namespace="CELERY")

#https://siddharth-pant.medium.com/the-missing-how-to-for-celery-logging-85e21f0231de
@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)


app.autodiscover_tasks()

