# Generated by Django 2.0.1 on 2018-01-20 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_article_total_subscriptions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
    ]
