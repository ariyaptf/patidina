# Generated by Django 4.1.1 on 2023-12-02 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('utils', '0012_alter_importantdaysinlunarcalendar_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importantdaysinlunarcalendar',
            name='article_page',
        ),
        migrations.RemoveField(
            model_name='importantdaysinlunarcalendar',
            name='details',
        ),
        migrations.CreateModel(
            name='LunarCalendarDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_text', models.CharField(max_length=255, verbose_name='detail')),
                ('article_page', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailcore.page', verbose_name='Article Page')),
                ('lunar_calendar_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='utils.importantdaysinlunarcalendar')),
            ],
        ),
    ]