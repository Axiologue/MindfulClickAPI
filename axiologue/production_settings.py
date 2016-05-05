from .base_settings import *

# Network settings
ALLOWED_HOSTS = ['api.axiologue.org', '104.236.76.8' ]

# DEBUG Tools
DEBUG = False

# Email settings
SITE_ID = 2
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = SECRETS['POSTMARK_KEY']
POSTMARK_SENDER = 'admin@axiologue.org'
POSTMARK_TRACK_OPENS = True

# Static Files Config
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'watched_file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/axiologue.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['watched_file',],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
