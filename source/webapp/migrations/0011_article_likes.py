# Generated by Django 4.2.2 on 2023-08-16 13:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0010_alter_article_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(related_name='likes_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
