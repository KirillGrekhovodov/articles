# Generated by Django 4.2.2 on 2023-07-05 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20230705_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='old_tags',
        ),
        migrations.DeleteModel(
            name='ArticleTag',
        ),
    ]