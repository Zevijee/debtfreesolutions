# Generated by Django 5.0.2 on 2024-02-19 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0015_ownerdata_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ownerdata',
            name='phone_number',
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_numbers', to='scraper.ownerdata')),
            ],
        ),
    ]
