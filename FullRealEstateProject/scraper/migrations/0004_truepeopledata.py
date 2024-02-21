# Generated by Django 5.0.2 on 2024-02-08 19:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_alter_ownerdata_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TruePeopleData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='true_people_data', to='scraper.ownerdata')),
            ],
        ),
    ]
