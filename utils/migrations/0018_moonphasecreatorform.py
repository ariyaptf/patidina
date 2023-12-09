# Generated by Django 4.1.1 on 2023-12-07 13:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0017_remove_importantdaysinsolarcalendar_article_page_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoonPhaseCreatorForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_date', models.DateField(default=django.utils.timezone.now)),
                ('before_selected_date', models.IntegerField(default=100)),
                ('after_selected_date', models.IntegerField(default=365)),
            ],
            options={
                'permissions': [('add', 'Add'), ('edit', 'Edit')],
            },
        ),
    ]
