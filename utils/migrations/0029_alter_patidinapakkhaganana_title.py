# Generated by Django 4.2.8 on 2023-12-12 13:33

from django.db import migrations, models
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0028_rename_name_patidinapakkhaganana_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patidinapakkhaganana',
            name='title',
            field=models.CharField(help_text='Enter the year in Buddhist Era format, which should be a 4-digit number and no less than 2500.', max_length=255, validators=[utils.models.validate_buddhist_year], verbose_name='title'),
        ),
    ]