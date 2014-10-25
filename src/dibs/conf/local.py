# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from configurations import values
from .common import Common


class Dev(Common):

    # SECURITY WARNING: don't run with debug turned on in production!
    # DEBUG
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # Mail settings
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
    # End mail settings

    INTERNAL_IPS = ('127.0.0.1',)


class Test(Dev):
    pass
