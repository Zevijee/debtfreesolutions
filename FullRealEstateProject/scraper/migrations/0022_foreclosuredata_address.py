# Generated by Django 5.0.2 on 2024-02-29 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0021_foreclosuredata'),
    ]

    operations = [
        migrations.AddField(
            model_name='foreclosuredata',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
