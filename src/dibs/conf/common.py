# encoding: utf-8
from __future__ import absolute_import, unicode_literals
"""
Django settings for dibs project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from configurations import Configuration, values

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Common(Configuration):

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'top-secret'

    # ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = (
        # 'django.contrib.admin.apps.AdminConfig',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'dibs',
        'dibsangular',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'dibs.urls'

    WSGI_APPLICATION = 'dibs.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/dev/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'TEST_NAME': ':memory:',
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/dev/topics/i18n/

    # LANGUAGE_CODE = 'en-us'

    # TIME_ZONE = 'UTC'

    # USE_I18N = True

    # USE_L10N = True

    # USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/dev/howto/static-files/

    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = '/tmp/static/'
    MEDIA_ROOT = '/tmp/media/'

    LOGIN_URL = 'login'
    LOGOUT_URL = 'logout'
    LOGIN_REDIRECT_URL = 'index'

    REST_FRAMEWORK = {
        # Use hyperlinked styles by default.
        # Only used if the `serializer_class` attribute is not set on a view.
        'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ]
    }
