# Generated by Django 5.1.6 on 2025-02-25 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0003_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('Mental Health', 'Mental Health'), ('Heart Disease', 'Heart Disease'), ('Covid19', 'Covid19'), ('Immunization', 'Immunization')], max_length=100),
        ),
    ]
