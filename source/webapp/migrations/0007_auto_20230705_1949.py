# Generated by Django 4.2.2 on 2023-07-05 13:49
from django.utils.text import slugify

from django.db import migrations


def set_title_slag_for_categories(apps, schema_editor):
    Category = apps.get_model('webapp.Category')
    for category in Category.objects.all():
        category.title_slug = slugify(category.title)
        category.save()


def rollback(apps, schema_editor):
    Category = apps.get_model('webapp.Category')
    for category in Category.objects.all():
        category.title_slug = None
        category.save()

class Migration(migrations.Migration):
    dependencies = [
        ('webapp', '0006_category_title_slug'),
    ]

    operations = [
        migrations.RunPython(set_title_slag_for_categories, rollback)
    ]