from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from dibs.api import ItemViewSet
from django.views.generic.base import RedirectView
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


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
             url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
             #url(r'^app/', include('dibsangular.urls')),
             url(r'^app/', include('dibsreact.urls')),
             )

urlpatterns += staticfiles_urlpatterns()

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += \
    patterns('',
             url(r'^$', RedirectView.as_view(permanent=False, pattern_name = 'index')),
             )
