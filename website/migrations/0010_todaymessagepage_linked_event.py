# Generated by Django 4.2.8 on 2023-12-16 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_remove_todaymessagepage_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todaymessagepage',
            name='linked_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='website.eventpage'),
        ),
    ]
