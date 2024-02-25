# Generated by Django 4.2.8 on 2024-02-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandham', '0003_alter_supportpublication_target_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportpublication',
            name='name',
            field=models.CharField(default='Anonymous', help_text='Please specify name, pseudonym, or dedication.', max_length=255, verbose_name='Name'),
        ),
    ]
