# Generated by Django 4.1.1 on 2023-12-02 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0015_remove_lunarcalendardetail_detail_text_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importantdaysinlunarcalendar',
            options={'ordering': ['lc_month', 'moon_phase', 'lc_day'], 'verbose_name': 'Important Days in Lunar Calendar', 'verbose_name_plural': 'Important Days in Lunar Calendar'},
        ),
        migrations.RenameField(
            model_name='importantdaysinlunarcalendar',
            old_name='moon_phase_lunar',
            new_name='moon_phase',
        ),
        migrations.RemoveField(
            model_name='importantdaysinlunarcalendar',
            name='day_adhikamasa',
        ),
        migrations.RemoveField(
            model_name='importantdaysinlunarcalendar',
            name='day_lunar',
        ),
        migrations.RemoveField(
            model_name='importantdaysinlunarcalendar',
            name='month_adhikamasa',
        ),
        migrations.RemoveField(
            model_name='importantdaysinlunarcalendar',
            name='month_lunar',
        ),
        migrations.AddField(
            model_name='importantdaysinlunarcalendar',
            name='lc_day',
            field=models.CharField(choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15')], default=0, max_length=2, verbose_name='day'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='importantdaysinlunarcalendar',
            name='lc_day_adhikamasa',
            field=models.CharField(choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15')], default=0, max_length=2, verbose_name='day'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='importantdaysinlunarcalendar',
            name='lc_month',
            field=models.CharField(choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '88'), ('10', '09'), ('11', '10'), ('12', '11'), ('13', '12')], default=0, max_length=2, verbose_name='month'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='importantdaysinlunarcalendar',
            name='lc_month_adhikamasa',
            field=models.CharField(choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '88'), ('10', '09'), ('11', '10'), ('12', '11'), ('13', '12')], default=0, max_length=2, verbose_name='month'),
            preserve_default=False,
        ),
    ]