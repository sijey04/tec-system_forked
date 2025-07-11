# Generated by Django 4.2 on 2025-07-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_alter_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('waiting_for_test_details', 'Waiting for Test Details'), ('waiting_for_submission', 'Waiting for Submission'), ('rejected', 'Rejected'), ('claimed', 'Claimed'), ('rescheduled', 'Rescheduled'), ('submitted', 'Submitted'), ('waiting_for_claiming', 'Waiting to be Claimed')], default='waiting_for_submission', max_length=30),
        ),
    ]
