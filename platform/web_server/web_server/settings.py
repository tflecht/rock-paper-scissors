from dotenv import load_dotenv
import logging
import os

from . import logging as project_logging

logger = logging.getLogger(__name__)
load_dotenv()

from web_server.config.base_dir import *
from web_server.config.celery import *
from web_server.config.discord import *
from web_server.config.staticfiles import *


# SECURITY WARNING: don't run with debug turned on in production!
PRODUCTION = (os.environ.get("PRODUCTION", 'TRUE') == 'TRUE')
DEBUG = (os.environ.get("DEBUG", 'FALSE') == 'TRUE')


# The root of all urls we serve up
BASE_URL = os.environ.get('BASE_URL', 'https://www.example.com')


LOGIN_REDIRECT_URL = '/users/login/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'django-insecure-jp^ef2&%y*degxe0w&=vxyuh8i*bgiez@^m2mk4-ud3ye8ur_$'
)

logger.info(f"runtime settings: PRODUCTION={PRODUCTION}, DEBUG={DEBUG}")

ALLOWED_HOSTS = [
    '*',
] if not DEBUG else ['*']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'bootstrap5',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
    'django_extensions',
    'modelcluster',
    'oauth2_provider',
    'polymorphic',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
]

SERVICE_APPS = [
    'discord',
    'game',
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + SERVICE_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'web_server.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web_server.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'helpers.views.default_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'web_server.context_processor.amplitude_settings',
                'web_server.context_processor.runtime_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'web_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# TIM - refactor so that the settings module doesn't need to worry
#     - about whether this is aws or not (encapsulate the handling of that).
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'admin',
            'PASSWORD': 'admin',
            'HOST': 'postgres',
            'PORT': 5432,
            'CONN_MAX_AGE': 0,
            'DISABLE_SERVER_SIDE_CURSORS': True,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
] if not DEBUG else []


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Pacific'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = project_logging.LOGGING


CORS_ALLOW_HEADERS = [
    'Access-Control-Allow-Credentials',
    'Authorization',
    'Content-Type',
    'X-CSRFToken',
]
CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-SessionId',
    'X-CSRFToken',
]
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = False
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ORIGIN_WHITELIST = (
)
OAUTH2_PROVIDER = {
    'REFRESH_TOKEN_EXPIRE_SECONDS': 360000,
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'},
    'ACCESS_TOKEN_EXPIRE_SECONDS': 1800
}
OAUTH_APP_CLIENT_ID = 'xi4Gps2AWLD7edHf02ry9yURA74BJAFZFPLsY88j'

# https://stackoverflow.com/questions/42818940/django-rest-framework-pagination-links-do-not-use-https
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')