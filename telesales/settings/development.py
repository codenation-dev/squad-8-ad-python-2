import os

from .base import *


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '08mivfb3r1_cl-)kk35kn6t(q0kgk50_kuidy@*+bsa6_5p=%c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_HOST_USER = 'sellgood@gmail.com'
EMAIL_HOST_PASSWORD = 'password'