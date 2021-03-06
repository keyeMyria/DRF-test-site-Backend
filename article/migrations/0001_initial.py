# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 20:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('theme', models.CharField(choices=[('#1976d2', 'Europa Universalis IV'), ('#82743B', 'Hearts of Iron 4'), ('#5C3B82', 'Other')], max_length=10)),
                ('primary_key', models.SlugField(editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.ArticleImage'),
        ),
    ]
