from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from dibs.api import ItemViewSet


api_router_v1 = routers.DefaultRouter()
api_router_v1.register(r'items', ItemViewSet)

admin.autodiscover()

urlpatterns = \
    patterns('',
             #     # Examples:
             #     # url(r'^$', 'dibs.views.home', name='home'),
             #     # url(r'^blog/', include('blog.urls')),
             url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
             url(r'^admin/', include(admin.site.urls)),
             url(r'^api/v1/', include(api_router_v1.urls)),
             url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
             )
