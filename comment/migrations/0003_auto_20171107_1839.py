# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_articlecomment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='comment.ArticleComment'),
        ),
    ]
