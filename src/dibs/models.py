from django.db import models
from django.conf import settings

_ = lambda x: x  # TODO: change it to lazy_ugettext


class Item(models.Model):
    name      = models.CharField(verbose_name=_('name'), max_length=255)
    parent    = models.ForeignKey('self', verbose_name=_('parent'), null=True, blank=True)
    dibbed_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  verbose_name=_('dibbed by'), null=True, blank=True)
    desc      = models.TextField(verbose_name=_('description'), null=True, blank=True)
