# Generated by Django 5.0.6 on 2024-09-15 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0038_remove_salesreport_delivered_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SalesReport',
        ),
    ]
