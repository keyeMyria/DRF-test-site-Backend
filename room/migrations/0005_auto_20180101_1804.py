# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-01 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_auto_20171230_0743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='created_date',
            new_name='created',
        ),
    ]
