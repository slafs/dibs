'''
WSGI config for dibs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
'''

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dibs.conf')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

# from django.core.wsgi import get_wsgi_application
from configurations.wsgi import get_wsgi_application  # noqa
application = get_wsgi_application()
