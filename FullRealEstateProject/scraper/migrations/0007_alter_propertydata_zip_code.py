# Generated by Django 5.0.2 on 2024-02-11 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_propertydata_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertydata',
            name='zip_code',
            field=models.CharField(default='11691', max_length=100),
            preserve_default=False,
        ),
    ]