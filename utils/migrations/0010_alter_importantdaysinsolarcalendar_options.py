# Generated by Django 4.1.1 on 2023-12-01 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0009_importantdaysinlunarcalendar_webpage_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importantdaysinsolarcalendar',
            options={'ordering': ['month', 'day'], 'verbose_name': 'Important Days in Solar Calendar', 'verbose_name_plural': 'Important Days in Solar Calendar'},
        ),
    ]
