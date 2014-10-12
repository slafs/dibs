# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dibs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='can_be_locked',
            field=models.NullBooleanField(default=None, help_text='can this item be set as locked?', verbose_name='can be locked'),
        ),
    ]
