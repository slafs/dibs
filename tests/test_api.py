#!/usr/bin/env python
# encoding: utf-8
"""
test_api
----------------------------------

Tests for `dibs.api` module.
"""

from dibs.models import Item
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
# from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import pytest

pytestmark = pytest.mark.django_db

UserModel = get_user_model()


class SimpleItemAPITestCase(APITestCase):

    def setUp(self):
        # create a user that can add items
        # and one test item and other user
        # both users can lock items
        perm_add = Permission.objects.get(codename='add_item')
        perm_lock = Permission.objects.get(codename='lock_item')

        self.user = UserModel.objects.create(username='testuser', password='password')
        self.user.user_permissions.add(perm_add, perm_lock)
        self.client.force_authenticate(user=self.user)
        self.user2 = UserModel.objects.create(username='otheruser', password='password')
        self.user2.user_permissions.add(perm_lock)
        self.item = Item.objects.create(name="simple testing item")

    def test_api_creation(self):

        url = '/api/v1/items/'
        res = self.client.post(url, {'name' : 'test item'})

        data = res.data
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('name'), 'test item')

    def test_lock_unlock_api_item(self):

        url = '/api/v1/items/{0}/lock/'.format(self.item.pk)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('status'), 'item locked')

        # try lock or unlock the same item as another user
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(user=self.user2)

        res2 = self.client.post(url)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res2.data.get('status'), 'item not locked')

        unlock_url = '/api/v1/items/{0}/unlock/'.format(self.item.pk)
        res3 = self.client.post(unlock_url)
        self.assertEqual(res3.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res3.data.get('status'), 'item not unlocked')

        # try to unlock the same item as the user who locked it
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(user=self.user)
        res4 = self.client.post(unlock_url)
        self.assertEqual(res4.status_code, status.HTTP_200_OK)
        self.assertEqual(res4.data.get('status'), 'item unlocked')
