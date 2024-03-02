# Generated by Django 5.0.2 on 2024-02-18 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0011_date_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100)),
                ('event', models.CharField(choices=[('option1', 'follow up call'), ('option2', 'reschedule appointment'), ('option3', 'needs visit'), ('option4', 'property appointment scheduled'), ('option5', 'contract signing'), ('option6', 'scheduled appraisle'), ('option7', 'scheduled inspection'), ('option8', 'scheduled cash for keys negotiation'), ('option9', 'scheduled closing')], max_length=100)),
                ('on_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='scraper.ownerdata')),
            ],
        ),
        migrations.DeleteModel(
            name='Date',
        ),
    ]
