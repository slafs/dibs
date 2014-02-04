#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dibs
----------------------------------

Tests for `dibs` module.
"""

from dibs.models import Item
from django.test import TestCase
# from django.conf import settings


class TestDibs(TestCase):

    def setUp(self):
        pass

    def test_something(self):
        item = Item(name="test item")
        item.save()
        self.assertTrue(item.pk is not None)

    def tearDown(self):
        pass
