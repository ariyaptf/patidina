# Generated by Django 4.2.8 on 2024-02-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandham', '0007_alter_supportpublication_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportpublication',
            name='target_groups',
            field=models.ManyToManyField(blank=True, help_text='Select the target groups for this support publication.', null=True, to='pandham.pandhamtargetgroup', verbose_name='Target Groups'),
        ),
    ]