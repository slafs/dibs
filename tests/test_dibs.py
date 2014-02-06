#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dibs
----------------------------------

Tests for `dibs` module.
"""

from dibs.models import Item
from django.conf import settings
import pytest
from django.db.models.loading import get_model

pytestmark = pytest.mark.django_db

UserModel = get_model(*settings.AUTH_USER_MODEL.rsplit('.', 1))


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
