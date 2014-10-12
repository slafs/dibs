# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(max_length=255, db_index=True, verbose_name='name')),
                ('desc', models.TextField(null=True, blank=True, verbose_name='description')),
                ('can_be_locked', models.NullBooleanField(help_text='whether or not an item can be set as locked.', default=None, verbose_name='can be locked')),
                ('locked_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='locked_items', null=True, blank=True, verbose_name='locked by')),
                ('parent', models.ForeignKey(to='dibs.Item', related_name='children', null=True, blank=True, verbose_name='parent')),
            ],
            options={
                'permissions': (('lock_item', 'Can lock an item'), ('unlock_foreign_item', 'Can unlock other users items')),
                'ordering': ['name'],
                'verbose_name_plural': 'items',
                'verbose_name': 'item',
            },
            bases=(models.Model,),
        ),
    ]
