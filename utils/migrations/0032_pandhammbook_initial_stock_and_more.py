# Generated by Django 4.2.8 on 2024-01-29 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_media', '0001_initial'),
        ('utils', '0031_pandhammbook_cover_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pandhammbook',
            name='initial_stock',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pandhammbook',
            name='cover_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_cover', to='custom_media.customimage'),
        ),
    ]