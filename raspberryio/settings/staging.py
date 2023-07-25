import json
import os

from ConfigParser import RawConfigParser

from raspberryio.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
        ('RaspberryIO Team', 'raspberryio-team@caktusgroup.com'),
    )
MANAGERS = ADMINS

DATABASES['default']['NAME'] = 'raspberryio_staging'

INSTALLED_APPS += (
    'gunicorn',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

EMAIL_SUBJECT_PREFIX = '[Raspberryio Staging] '

# Django Compressor configuration
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# Setup SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# import secrets
try:
    SECRETS_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    config = RawConfigParser()
    config.read(os.path.join(SECRETS_ROOT, 'settings.ini'))
    SUPERFEEDR_CREDS = json.loads(config.get('secrets', 'SUPERFEEDR_CREDS'))
    SECRET_KEY = json.loads(config.get('secrets', 'SECRET_KEY'))
except:
    pass

# Disqus
DISQUS_SHORTNAME = 'raspberryio-staging'
