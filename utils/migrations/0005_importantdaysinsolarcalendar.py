# Generated by Django 4.1.1 on 2023-12-01 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_alter_importantdaysinlunarcalendar_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantDaysInSolarCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solar_date', models.DateField(blank=True, null=True, verbose_name='solar date')),
                ('details', models.TextField(max_length=255, verbose_name='details')),
            ],
            options={
                'verbose_name': 'Important Days in Solar Calendar',
                'verbose_name_plural': 'Important Days in Solar Calendar',
            },
        ),
    ]