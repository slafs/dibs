from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = \
    patterns('',
             url(r'accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'dibsreact/login.html'}, name="login"),
             url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
             url(r'^$', TemplateView.as_view(template_name='dibsreact/app.html'), name='index'),
             )
