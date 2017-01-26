import os

from .base_settings import *

# Network settings
ALLOWED_HOSTS = ['*']

# Static Files Config
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# DEBUG tools 
DEBUG = True

# django-debug-toolbar settings
INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}

INTERNAL_IPS = ('127.0.0.1','::ffff:10.0.2.2')


# overwrite url_config with dev version
ROOT_URLCONF = 'mindfulclick.dev_urls'

# Email settings
SITE_ID = 3
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'http://localhost:9000/#/login'

