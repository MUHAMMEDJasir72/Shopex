# Generated by Django 5.0.6 on 2024-09-03 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0036_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='offer_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
