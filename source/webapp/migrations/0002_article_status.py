# Generated by Django 4.2.2 on 2023-06-21 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('new', 'Новая'), ('moderated', 'Модерированная'), ('deleted', 'Удаленная')], default='new', max_length=20, verbose_name='Статус'),
        ),
    ]