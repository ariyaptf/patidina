# Generated by Django 4.1.1 on 2023-12-01 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_alter_importantdaysinlunarcalendar_lunar_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importantdaysinlunarcalendar',
            name='details',
            field=models.TextField(max_length=255, verbose_name='details'),
        ),
    ]
