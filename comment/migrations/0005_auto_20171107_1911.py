# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20171107_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_comment', to='comment.ArticleComment'),
        ),
    ]
