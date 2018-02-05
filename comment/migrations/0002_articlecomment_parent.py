# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='parent',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='comment.ArticleComment'),
            preserve_default=False,
        ),
    ]
