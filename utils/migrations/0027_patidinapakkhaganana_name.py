# Generated by Django 4.2.8 on 2023-12-12 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0026_patidinapakkhaganana_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patidinapakkhaganana',
            name='name',
            field=models.CharField(default=0, max_length=255, verbose_name='title'),
            preserve_default=False,
        ),
    ]
