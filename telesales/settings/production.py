import os

import dj_database_url
from decouple import config

from .base import *

ALLOWED_HOSTS = ['.herokuapp.com']

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE.append(
  'whitenoise.middleware.WhiteNoiseMiddleware',
)

DATABASES = {
    'default': dj_database_url.config()
}

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config(('EMAIL_HOST_PASSWORD')
