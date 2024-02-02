# Generated by Django 4.2.8 on 2024-01-30 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0032_pandhammbook_initial_stock_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PanDhammTargetGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Group Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'PanDhamm Target Group',
                'verbose_name_plural': 'PanDhamm Target Groups',
            },
        ),
        migrations.CreateModel(
            name='SupportPublication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('date_contribute', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('amount_contributed', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('distribution_preference', models.CharField(choices=[('request_book', 'Request Book'), ('no_book_request', 'No Book Requested')], max_length=100, verbose_name='Distribution Preference')),
                ('requested_books', models.PositiveIntegerField(default=0, verbose_name='Requested Books')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('shipping_address', models.TextField(verbose_name='Shipping Address')),
                ('otp', models.CharField(max_length=6, verbose_name='OTP Number')),
                ('pandhann_books', models.PositiveIntegerField(default=0, verbose_name='PanDhamm Books')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_publication', to='utils.pandhammbook', verbose_name='PanDhamm Book')),
                ('target_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utils.pandhammtargetgroup', verbose_name='Target Group')),
            ],
            options={
                'verbose_name': 'Support Publication',
                'verbose_name_plural': 'Support Publications',
            },
        ),
        migrations.CreateModel(
            name='PanDhammTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address', models.TextField(verbose_name='Address')),
                ('requested_books', models.PositiveIntegerField(verbose_name='Requested Books')),
                ('request_date', models.DateTimeField(verbose_name='Request Date')),
                ('additional_info', models.TextField(blank=True, verbose_name='Additional Information')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='utils.pandhammtargetgroup', verbose_name='Target Group')),
            ],
            options={
                'verbose_name': 'PanDhamm Target',
                'verbose_name_plural': 'PanDhamm Targets',
            },
        ),
    ]
