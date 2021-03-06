# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 17:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0005_auto_20171102_1530'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
