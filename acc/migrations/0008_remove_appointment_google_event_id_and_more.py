# Generated by Django 5.1.6 on 2025-03-04 17:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0007_alter_appointment_doctor_alter_appointment_end_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='google_event_id',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='speciality',
            field=models.CharField(max_length=100),
        ),
    ]
