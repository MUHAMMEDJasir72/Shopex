# Generated by Django 5.0.6 on 2024-09-11 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0055_remove_order_offer_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
    ]
