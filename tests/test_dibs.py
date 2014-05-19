#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_dibs
----------------------------------

Tests for `dibs` module.
'''

from dibs.models import Item
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
import pytest

pytestmark = pytest.mark.django_db

UserModel = get_user_model()


@pytest.fixture
def dibs_user(username='testuser'):
    perm_add = Permission.objects.get(codename='add_item')
    perm_lock = Permission.objects.get(codename='lock_item')

    user = UserModel.objects.create(username=username, password='password')
    user.user_permissions.add(perm_add, perm_lock)
    return user


def test_simple_save():
    item = Item(name='test item')
    item.save()
    assert (item.pk is not None)


def test_simple_tree(dibs_user):
    user = dibs_user

    pitem1 = Item.objects.create(name='test item 1')
    pitem2 = Item.objects.create(name='test item 2')
    Item.objects.create(name='child item 1', parent = pitem1)
    Item.objects.create(name='child item 2', parent = pitem2)

    qs = Item.objects.all()
    assert (qs.count() == 4)

    item = Item.objects.get(name='child item 1')

    how_many = item.lock(user)
    assert how_many == 1

    item = Item.objects.get(name='child item 1')
    assert item.locked_by == user

    qs = Item.objects.locked_by_user(user)
    assert qs.count() == 1

    item.unlock(user)

    item = Item.objects.get(name='child item 1')
    assert item.locked_by is None


def test_simple_lock_block(dibs_user):
    item = Item.objects.create(name='test item', can_be_locked=False)
    user = dibs_user

    assert item.lockable is False
    count = item.lock(user)
    assert count == 0


def test_unlock_foreign_item():
    item = Item.objects.create(name='test item')

    user1 = dibs_user('firstuser')
    user2 = dibs_user('seconduser')

    # item can be locked
    assert item.lockable is True

    count = item.lock(user1)
    assert count == 1

    # now item can't be locked
    item = Item.objects.get(name='test item')

    assert item.lockable is False
    count = item.lock(user2)
    assert count == 0
    assert item.locked_by == user1

    # no matter who wants to lock it
    count = item.lock(user1)
    assert count == 0

    # no other user can unlock other item
    count = item.unlock(user2)
    assert count == 0
    count = item.unlock(user1)
    assert count == 1


def test_permission_unlock_foreign_item():
    item = Item.objects.create(name='test item')
    user = dibs_user()
    super_user = dibs_user(username='seconduser')

    count = item.lock(user)
    assert count == 1

    # without permission second user can't unlock item
    count = item.unlock(super_user)
    assert count == 0

    # but when a user gets a permission to unlock it
    perm = Permission.objects.get(codename='unlock_foreign_item')
    super_user.user_permissions.add(perm)

    # then the user should unlock the item
    super_user = UserModel.objects.get(username='seconduser')
    count = item.unlock(super_user)
    assert count == 1

    item = Item.objects.get(name='test item')
    assert item.lockable is True
