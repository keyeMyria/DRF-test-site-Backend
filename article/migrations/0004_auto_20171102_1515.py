# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20171102_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='theme',
            field=models.CharField(choices=[('Europa Universalis IV', 'Europa Universalis IV'), ('Hearts of Iron 4', 'Hearts of Iron 4'), ('Offtop', 'Other')], max_length=10),
        ),
    ]
