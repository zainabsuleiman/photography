# Generated by Django 3.2 on 2023-06-24 12:43

import client.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments_uploads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_result', models.ImageField(default=None, null=True, upload_to=client.models.wrapper)),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.appointment')),
            ],
            options={
                'db_table': 'Appointment_uploads',
            },
        ),
    ]