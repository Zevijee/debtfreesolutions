# Generated by Django 5.0.2 on 2024-02-29 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0020_event_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeclosureData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction_date', models.CharField(blank=True, max_length=100, null=True)),
                ('auction_time', models.CharField(blank=True, max_length=100, null=True)),
                ('auction_location', models.CharField(blank=True, max_length=255, null=True)),
                ('date_added', models.CharField(blank=True, max_length=100, null=True)),
                ('plaintiff', models.CharField(blank=True, max_length=255, null=True)),
                ('defendant', models.CharField(blank=True, max_length=255, null=True)),
                ('lien', models.CharField(blank=True, max_length=100, null=True)),
                ('judgment', models.CharField(blank=True, max_length=100, null=True)),
                ('index_no', models.CharField(blank=True, max_length=100, null=True)),
                ('referee', models.CharField(blank=True, max_length=100, null=True)),
                ('plaintiff_attorney', models.CharField(blank=True, max_length=255, null=True)),
                ('plaintiff_attorney_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('foreclosure_type', models.CharField(blank=True, max_length=100, null=True)),
                ('auction_notes', models.CharField(blank=True, max_length=255, null=True)),
                ('unit_number', models.CharField(blank=True, max_length=100, null=True)),
                ('previously_scheduled_on', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
