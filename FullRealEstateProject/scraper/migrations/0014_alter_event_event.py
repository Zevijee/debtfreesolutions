# Generated by Django 5.0.2 on 2024-02-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0013_event_owner_alter_event_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event',
            field=models.CharField(blank=True, choices=[('follow_up_call', 'follow up call'), ('reschedule_appointment', 'reschedule appointment'), ('needs_visit', 'needs visit'), ('property_appointment_scheduled', 'property appointment scheduled'), ('contract_signing', 'contract signing'), ('scheduled_appraisal', 'scheduled appraisal'), ('scheduled_inspection', 'scheduled inspection'), ('scheduled_cash_for_keys_negotiation', 'scheduled cash for keys negotiation'), ('scheduled_closing', 'scheduled closing')], max_length=100, null=True),
        ),
    ]
