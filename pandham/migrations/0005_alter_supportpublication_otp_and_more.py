# Generated by Django 4.2.8 on 2024-02-19 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandham', '0004_alter_supportpublication_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportpublication',
            name='otp',
            field=models.CharField(help_text='Enter the OTP number.', max_length=6, verbose_name='OTP'),
        ),
        migrations.AlterField(
            model_name='supportpublication',
            name='phone_number',
            field=models.CharField(help_text='Contactable mobile phone number ie.0988888888 (not publicly disclosed).', max_length=20, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='supportpublication',
            name='requested_books',
            field=models.PositiveIntegerField(default=0, help_text='Enter the number of books requested.', verbose_name='Requested Books'),
        ),
    ]
