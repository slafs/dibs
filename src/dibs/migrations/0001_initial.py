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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='name', db_index=True)),
                ('desc', models.TextField(null=True, verbose_name='description', blank=True)),
                ('can_be_locked', models.NullBooleanField(default=None, help_text='whether or not an item can be set as locked.', verbose_name='can be locked')),
                ('locked_by', models.ForeignKey(verbose_name='locked by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name=b'children', verbose_name='parent', blank=True, to='dibs.Item', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'permissions': (('lock_item', 'Can lock an item'), ('unlock_foreign_item', 'Can unlock other users items')),
            },
            bases=(models.Model,),
        ),
    ]
