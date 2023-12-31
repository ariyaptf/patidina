# Generated by Django 4.1.1 on 2023-12-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_importantdaysinsolarcalendar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importantdaysinsolarcalendar',
            name='solar_date',
        ),
        migrations.AddField(
            model_name='importantdaysinsolarcalendar',
            name='day',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)], null=True, verbose_name='day'),
        ),
        migrations.AddField(
            model_name='importantdaysinsolarcalendar',
            name='month',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], null=True, verbose_name='month'),
        ),
    ]
