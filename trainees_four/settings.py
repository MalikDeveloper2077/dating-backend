import os
import sys

from envparse import env
import dj_database_url


env.read_envfile('../trainees_four/conf/config.env')


DATA_UPLOAD_MAX_NUMBER_FIELDS = 500000000
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING_LEVEL = env.str('LOGGING_LEVEL', default='INFO')

BASE_URL = env.str('BASE_URL')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
)


ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 10


INSTALLED_APPS = [
    'adminactions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # our apps
    'members.apps.MembersConfig',
    'products.apps.ProductsConfig',

    # third-party
    'admintools',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters'
]


SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


ROOT_URLCONF = 'trainees_four.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]


WSGI_APPLICATION = 'trainees_four.wsgi.application'


DATABASES = {
    'default':  dj_database_url.parse(
        env.str('DATABASE_URL'), conn_max_age=30),
}


AUTH_USER_MODEL = 'members.Member'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # noqa
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Email setup
EMAIL_BACKEND = env.str('EMAIL_BACKEND')
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT', default=2525)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)


# Static and media
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
                '%(asctime)s [%(levelname)s] %(ip)s %(email)s '
                '%(pathname)s:%(lineno)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'admintools': {
            'handlers': ['console',],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console',],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'local_caching',
    },
    'snowflake': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 5*60,  # 5*60 = 5 minutes
    },
    'longhorn': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table_for_django',
        'TIMEOUT': 1*60*60,  # 1*60*60 = 1 hour
    },
}
