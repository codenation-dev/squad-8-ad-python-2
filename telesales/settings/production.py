import os
import dj_database_url

from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE.append(
  'whitenoise.middleware.WhiteNoiseMiddleware',
)

DATABASES = {
    'default': dj_database_url.config()
}

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')