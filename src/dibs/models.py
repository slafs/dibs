# encoding: utf-8
from __future__ import print_function, absolute_import, division, unicode_literals
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
# import mptt
# from mptt.fields import TreeForeignKey
# from mptt.managers import TreeManager


class ItemQuerySet(QuerySet):

    def locked_by_user(self, user):
        '''
        Get items that are locked by a given user
        '''
        return self.filter(locked_by=user)

    def potentially_lockable(self):
        '''
        Returns a queryset of a potentially lockable objects.
        It checks a ``can_be_locked`` attribute
        '''
        return self.filter(Q(can_be_locked=True) | Q(can_be_locked__isnull=True))

    def lockable(self):
        '''
        Returns a queryset of lockable objects
        i.e. potentially lockable objects (see ``potentially_lockable``)
        that aren't locked by anyone else
        '''
        qs = self.potentially_lockable()
        return qs.filter(locked_by__isnull=True)

    def lock(self, pk, user=None):
        '''
        Locks an item by it's primary key (only if it can be locked)

        .. warning::
            this method doesn't return a QuerySet

        returns the number of items that were locked
        '''
        if user and not user.has_perm('dibs.lock_item'):
            return 0

        qs = self.lockable()
        return qs.filter(pk=pk).update(locked_by=user)

    def unlock(self, pk, user=None):
        '''
        Unlocks an item by it's primary key (only if it is locked by the given user)

        .. warning::
            this method doesn't return a QuerySet

        returns the number of items that were unlocked
        '''
        filter_dict = {}
        if pk is not None:
            filter_dict.update({'pk': pk})

        if pk is None or (user is not None and not user.has_perm('dibs.unlock_foreign_item')):
            filter_dict.update({'locked_by': user})

        qs = self.filter(**filter_dict)
        return qs.update(locked_by=None)


class Item(TimeStampedModel):
    '''
    Main model for stuff that can be "dibbed" (locked)
    '''
    name      = models.CharField(_('name'), max_length=255, db_index=True)
    parent    = models.ForeignKey('self', verbose_name=_('parent'),
                                  null=True, blank=True, related_name='children')
    locked_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  verbose_name=_('locked by'), null=True, blank=True,
                                  related_name='locked_items')
    desc      = models.TextField(_('description'), null=True, blank=True)

    can_be_locked = \
        models.NullBooleanField(_('can be locked'), default=None,
                                help_text=_('whether or not an item can be set as locked.'))

    objects = ItemQuerySet.as_manager()
    # tree_manager = TreeManager()

    def __unicode__(self):
        return self.name

    @property
    def lockable(self):
        '''
        convieniance property indicating whether or not an item can be locked

        :return type: bool
        '''
        if self.can_be_locked is None or self.can_be_locked is True:
            return self.locked_by is None
        else:
            return False

    def lock(self, user=None):
        '''
        main method for locking an item
        '''
        if self.pk is None:  # object must be in DB
            return 0
        return Item.objects.lock(self.pk, user=user)

    def unlock(self, user=None):
        '''
        complementary method for unlocking an item
        '''
        if self.pk is None:  # object must be in DB
            return 0
        return Item.objects.unlock(self.pk, user=user)

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        permissions = (
            ("lock_item", "Can lock an item"),
            ("unlock_foreign_item", "Can unlock other users items"),
        )
        ordering = ['name']

# register mptt
# TreeForeignKey(Item, verbose_name=_('parent'), null=True, blank=True,
#                related_name='children').contribute_to_class(Item, 'parent')
# mptt.register(Item, order_insertion_by=['name'])


# def mark_nodes(queryset=None):
#     '''
#     sets all leafs items ``can_be_locked`` attribute to True
#     and all non-leafs to False if and only if they haven't been set earlier
#     '''
#     if queryset is not None:
#         qs = queryset
#     else:
#         qs = Item.tree_manager.root_nodes()
#     # TODO: finish this when implementing bulk importing (e.g. from a file)
#     for root in qs:
#         leafnodes = root.get_leafnodes()
#         leafnodes.filter(can_be_locked__isnull=True).update(can_be_locked=True)
