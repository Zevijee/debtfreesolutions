# Generated by Django 5.0.2 on 2024-02-20 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0018_truepeopledata_data_found'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='state',
            field=models.CharField(blank=True, default='unknown', max_length=100, null=True),
        ),
    ]
