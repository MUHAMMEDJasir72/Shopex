# Generated by Django 5.0.6 on 2024-09-11 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0054_remove_transaction_transaction_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='offer_price',
        ),
    ]
