# Generated by Django 4.1.1 on 2023-12-01 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0007_alter_importantdaysinsolarcalendar_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importantdaysinlunarcalendar',
            name='lunar_date',
            field=models.CharField(max_length=25, null=True, verbose_name='lunar date'),
        ),
        migrations.AlterField(
            model_name='importantdaysinlunarcalendar',
            name='lunar_date_in_adhikamasa',
            field=models.CharField(max_length=255, null=True, verbose_name='lunar date in adhikamasa'),
        ),
        migrations.AlterField(
            model_name='importantdaysinsolarcalendar',
            name='day',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)], null=True, verbose_name='day'),
        ),
        migrations.AlterField(
            model_name='importantdaysinsolarcalendar',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], null=True, verbose_name='month'),
        ),
    ]
