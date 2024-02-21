# Generated by Django 5.0.2 on 2024-02-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_alter_propertydata_building_sqft_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerdata',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='previousfilings',
            name='filing_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='previousfilings',
            name='filing_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]