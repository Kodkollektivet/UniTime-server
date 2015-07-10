# -*- coding:utf-8 -*-

"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
n
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r86a2f9n^+m$&8)u0j9%39s7*v_7#a2sp^*j3tvx_9w*16p0(q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'compressor',
    
    'timeedit',
    'angular',
    'courserate',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


STATICFILES_FINDERS=(
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


COMPRESS_ENABLED = True
#COMPRESS_OFFLINE = True


ROOT_URLCONF = 'settings.urls'

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

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'unitime',
        'USER': 'unitime',
        'PASSWORD': 'EA892DB71728C3E29ACC0BD16A3BC21670C16998F0A13AE6C042D83C8B1F3780',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

# Crispyforms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'


LOGGING = {
    'version':1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        # Default log
        'default': {
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'log/debug.log',
            'maxBytes' : 1024 * 1024 * 5, # 5BM
            'backupCount' : 5,
            'formatter' : 'standard',
        },
        # Debug log for django requests
        'request_handler': {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'log/requests.log',
            'maxBytes' : 1024 * 1024 * 5, # 5MB
            'backupCount' : 5,
            'formatter': 'standard'
        },
        # Logs only search terms from the view
        'search_handler': {
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'log/search.log',
            'maxBytes' : 1024 * 1024 * 5, # 5MB
            'backupCount' : 5,
            'formatter': 'standard'
        },
        # For logging mismatching course codes
        'error_Handler' : {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'log/mismatch.log',
            'maxBytes' : 1024 * 1024 * 5, # 5MB
            'backupCount' : 5,
            'formatter': 'standard'
        },
    },
    'loggers': {
        
        'defaultLogger': {
            'handlers' : ['default'],
            'level' : 'INFO',
            'propagate' : True
        },
        'django.request' : {
            'handlers' : ['request_handler'],
            'level' : 'DEBUG',
            'propagate' : False
        },
        'searchLogger': {
            'handlers' : ['search_handler'],
            'level' : 'INFO',
            'propagate' : False
        },
        'errorLogger' : {
            'handlers' : ['error_Handler'],
            'level' : 'INFO',
            'propagate' : False
        }
    }
}
