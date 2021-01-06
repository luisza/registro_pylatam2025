"""
Django settings for ECSL project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from __future__ import absolute_import
import os
from django.urls.base import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADMINS = (
    ('Luis', 'luisza14@gmail.com'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5)%f%3ng*4981z7w6n3b_@_ctfmlzw(+thct%x!agmn%hwt(l1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
DEBUG_TOOLBAR = os.getenv('DEBUG_TOOLBAR', 'false').lower() == 'true'

if os.getenv('ALLOWED_HOSTS', ''):
    ALLOWED_HOSTS = [c for c in os.getenv('ALLOWED_HOSTS', '').split(',')]
else:
    ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = [
    'ecsl',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_registration',
    "bootstrapform",

    # 'osem',
    'proposal',
    'crispy_forms',
    'ajax_select',
    'async_notifications',
    'ckeditor',
    'ckeditor_uploader',
    'django_celery_beat',
]

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG_TOOLBAR:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]

ROOT_URLCONF = 'ECSL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ECSL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME', 'ecsl'),
        'USER': os.getenv('DB_USER', 'ecsl'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'ecsl'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT':  int(os.getenv('DB_PORT', '3306'))
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Costa_Rica'

USE_I18N = True

USE_L10N = True

USE_TZ = True
ACCOUNT_ACTIVATION_DAYS = 2


LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
CKEDITOR_UPLOAD_PATH = "uploads/"

EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')  # mail service smtp
EMAIL_PORT = os.getenv('EMAIL_PORT', '1025')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)  # a real email
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Registro ECSL <not-reply@softwarelibre.ca>')


MAX_INSCRIPTION = 250
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]


CELERY_MODULE = "ECSL.celery"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # execute 12:30 pm
    'send_daily_emails': {
        'task': 'async_notifications.tasks.send_daily',
        'schedule': crontab(minute='*/10',),
    },
}

ASYNC_NOTIFICATION_TEXT_AREA_WIDGET = 'ckeditor.widgets.CKEditorWidget'
ASYNC_NOTIFICATION_MAX_PER_MAIL = 5

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'db+mysql://guest:guest@localhost:5672/ecsl')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'db+mysql://guest:guest@localhost:5672/ecslresult')
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH=191

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'organilab': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
