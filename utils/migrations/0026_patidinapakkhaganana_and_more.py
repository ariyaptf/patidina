# Generated by Django 4.2.8 on 2023-12-12 13:11

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0025_importantdaysinlunarcalendar_lunar_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatidinaPakkhaganana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Paṭidina Pakkhagaṇanā',
                'verbose_name_plural': 'Paṭidina Pakkhagaṇanā',
            },
        ),
        migrations.AlterField(
            model_name='importantdaysinlunarcalendar',
            name='moon_phase',
            field=models.CharField(choices=[('01', 'ขึ้น'), ('02', 'แรม')], default='01', max_length=10, verbose_name='moon phase'),
        ),
        migrations.AlterField(
            model_name='importantdaysinlunarcalendar',
            name='moon_phase_adhikamasa',
            field=models.CharField(choices=[('01', 'ขึ้น'), ('02', 'แรม')], default='01', max_length=10, verbose_name='moon phase'),
        ),
        migrations.CreateModel(
            name='UposathaOfPakkhaganana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('selected_date', models.DateField()),
                ('moon_phase', models.CharField(choices=[('last_quarter', 'จันทร์ลับ'), ('new_moon', 'จันทร์ดับ'), ('first_quarter', 'จันทร์กึ่ง'), ('full_moon', 'จันทร์เพ็ญ')], max_length=15, verbose_name='moon phase')),
                ('patidina_pakkhaganana', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='uposatha_of_pakkhaganana', to='utils.patidinapakkhaganana', verbose_name='Uposatha Day')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
