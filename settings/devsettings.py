# -*- coding:utf-8 -*-
from .settings import *
"""
Dev settings
"""

DEBUG = True


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



COMPRESS_ENABLED = False

# Logging
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
            'filename' : 'timeedit/logs/debug.log',
            'maxBytes' : 1024 * 1024 * 5, # 5BM
            'backupCount' : 5,
            'formatter' : 'standard',
        },
        # Debug log for django requests
        'request_handler': {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'timeedit/logs/requests.log',
            'maxBytes' : 1024 * 1024 * 5, # 5MB
            'backupCount' : 5,
            'formatter': 'standard'
        },
        # Logs only search terms from the view
        'search_handler': {
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'timeedit/logs/search.log',
            'maxBytes' : 1024 * 1024 * 5, # 5MB
            'backupCount' : 5,
            'formatter': 'standard'
        },
        # For logging mismatching course codes
        'error_Handler' : {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : 'timeedit/logs/mismatch.log',
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