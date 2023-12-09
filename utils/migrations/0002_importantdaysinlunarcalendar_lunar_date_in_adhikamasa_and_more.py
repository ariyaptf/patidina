# Generated by Django 4.1.1 on 2023-12-01 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='importantdaysinlunarcalendar',
            name='lunar_date_in_adhikamasa',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='lunar date in adhikamasa'),
        ),
        migrations.AlterField(
            model_name='importantdaysinlunarcalendar',
            name='details',
            field=models.CharField(max_length=255, verbose_name='details'),
        ),
        migrations.AlterField(
            model_name='importantdaysinlunarcalendar',
            name='lunar_date',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='lunar date'),
        ),
    ]
