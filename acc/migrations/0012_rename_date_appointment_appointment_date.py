# Generated by Django 5.1.6 on 2025-03-05 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0011_remove_doctor_speciality_remove_doctor_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='date',
            new_name='appointment_date',
        ),
    ]
