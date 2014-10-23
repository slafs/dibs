# encoding: utf-8
# from __future__ import print_function, absolute_import, division, unicode_literals

import os
import crochet
crochet.no_setup()

from twisted.application import internet, service
from twisted.web import server, wsgi, static  # , resource
from twisted.python import threadpool
from twisted.internet import reactor  # , protocol

from django.conf import settings

from dibs import twresource

PORT = 8000


class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()

# Environment setup for your Django project files:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dibs.conf')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

from configurations import importer
importer.install()

from django.core.handlers.wsgi import WSGIHandler
import django
django.setup()

# Twisted Application Framework setup:
application = service.Application('twisted-django-dibs')


# WSGI container for Django, combine it with twisted.web.Resource:
# XXX this is the only 'ugly' part: see the 'getChild' method in twresource.Root
# The MultiService allows to start Django and Twisted server as a daemon.

multi = service.MultiService()
pool = threadpool.ThreadPool()
tps = ThreadPoolService(pool)
tps.setServiceParent(multi)
resource = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
root = twresource.Root(resource)

# Servce Django media files off of /media:
mediasrc = static.File(settings.MEDIA_ROOT)
staticsrc = static.File(settings.STATIC_ROOT)

# root.putChild("media", mediasrc)
# root.putChild("static", staticsrc)

root.putChild(settings.MEDIA_URL.replace('/', ''), mediasrc)
root.putChild(settings.STATIC_URL.replace('/', ''), staticsrc)

# The cool part! Add in pure Twisted Web Resouce in the mix
# This 'pure twisted' code could be using twisted's XMPP functionality, etc:
root.putChild("stream", twresource.sse_resource)

# Serve it up:
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(multi)
multi.setServiceParent(application)
