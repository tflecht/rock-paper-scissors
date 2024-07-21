from dotenv import load_dotenv
import os

load_dotenv()


#############################################################
# Sentry Configuration
#############################################################
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

SENTRY_DSN_URL = os.environ.get('SENTRY_DSN_URL', None)
SENTRY_ENVIRONMENT = os.environ.get('SENTRY_ENVIRONMENT', 'unknown')

if SENTRY_DSN_URL:
    # Config options: https://docs.sentry.io/platforms/python/guides/django/configuration/options/
    sentry_sdk.init(
        dsn=SENTRY_DSN_URL,
        environment=SENTRY_ENVIRONMENT,
        integrations=[
            CeleryIntegration(),
            DjangoIntegration(
                transaction_style='url',
            ),
            RedisIntegration(),
        ],
        request_bodies='always',

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
