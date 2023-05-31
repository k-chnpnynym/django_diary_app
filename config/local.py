from .base import *

# 通常の console だと日本語メールのタイトルが文字化けしてしまうので回避
# ref: https://speakerdeck.com/thinkami/djangocongress-jp-2019-talk?slide=44
#      https://speakerdeck.com/thinkami/djangocongress-jp-2019-talk?slide=45
#      https://speakerdeck.com/thinkami/djangocongress-jp-2019-talk?slide=46
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'config.email_backends.ReadableSubjectEmailBackend'

##################
# MEDIA settings #
##################
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR

DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': 'mytestdb',
        }}
}

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ["127.0.0.1", ]  # debug toolbar