from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

DEBUG = False

ALLOWED_HOSTS = [env('ALLOWED_HOSTS'), ]


##################
# AWS settings #
##################

##################
# Static files #
##################

# STATIC_ROOT = '/var/www/mysite/static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'mysite-static-storage-sumiteru'
AWS_DEFAULT_ACL = None


##################
# Media files #
##################

# MEDIA_ROOT = '/var/www/mysite/media'
DEFAULT_FILE_STORAGE = 'config.storage_backends.S3MediaStorage'
MEDIA_AWS_STORAGE_BUCKET_NAME = 'mysite-media-storage-sumiteru'
MEDIA_AWS_DEFAULT_ACL = None


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'ATOMIC_REQUESTS': True,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(process)s %(thread)d %(pathname)s:%(lineno)d %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/mysite/app.log',
            'formatter': 'production',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 10 * 10  # 2.5M×10=250M
FILE_UPLOAD_PERMISSIONS = 0o777
