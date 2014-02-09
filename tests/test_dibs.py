#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dibs
----------------------------------

Tests for `dibs` module.
"""

from dibs.models import Item
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
import pytest

pytestmark = pytest.mark.django_db

UserModel = get_user_model()


def test_simple_save():
    item = Item(name="test item")
    item.save()
    assert (item.pk is not None)


def test_simple_tree():
    pitem1 = Item.objects.create(name="test item 1")
    pitem2 = Item.objects.create(name="test item 2")
    Item.objects.create(name="child item 1", parent = pitem1)
    Item.objects.create(name="child item 2", parent = pitem2)

    qs = Item.objects.all()
    assert (qs.count() == 4)

    user = UserModel.objects.create(username="testuser")
    item = Item.objects.get(name="child item 1")

    how_many = Item.objects.lock(user, item.pk)
    assert how_many == 1

    item = Item.objects.get(name="child item 1")
    assert item.locked_by == user

    qs = Item.objects.locked_by_user(user)
    assert qs.count() == 1

    Item.objects.unlock(user, item.pk)
    item = Item.objects.get(name="child item 1")
    assert item.locked_by is None


def test_simple_lock_block():
    item = Item.objects.create(name="test item", can_be_locked=False)
    user = UserModel.objects.create(username="testuser")

    assert item.lockable is False
    count = Item.objects.lock(user, pk=item.pk)
    assert count == 0


def test_unlock_foreign_item():
    item = Item.objects.create(name="test item")
    user1 = UserModel.objects.create(username="firstuser")
    user2 = UserModel.objects.create(username="seconduser")

    # item can be locked
    assert item.lockable is True

    count = Item.objects.lock(user1, pk=item.pk)
    assert count == 1

    # now item can't be locked
    item = Item.objects.get(name="test item")

    assert item.lockable is False
    count = Item.objects.lock(user2, pk=item.pk)
    assert count == 0
    assert item.locked_by == user1

    # no matter who wants to lock it
    count = Item.objects.lock(user1, pk=item.pk)
    assert count == 0

    # no other user can unlock other item
    count = Item.objects.unlock(user2, pk=item.pk)
    assert count == 0
    count = Item.objects.unlock(user1, pk=item.pk)
    assert count == 1


def test_permission_unlock_foreign_item():
    item = Item.objects.create(name="test item")
    user = UserModel.objects.create(username="firstuser")
    super_user = UserModel.objects.create(username="seconduser")

    count = Item.objects.lock(user, pk=item.pk)
    assert count == 1

    # without permission second user can't unlock item
    count = Item.objects.unlock(super_user, pk=item.pk)
    assert count == 0

    # but when a user gets a permission to unlock it
    perm = Permission.objects.get(codename='unlock_foreign_item')
    super_user.user_permissions.add(perm)

    # then the user should unlock the item
    super_user = UserModel.objects.get(username="seconduser")
    count = Item.objects.unlock(super_user, pk=item.pk)
    assert count == 1

    item = Item.objects.get(name="test item")
    assert item.lockable is True
