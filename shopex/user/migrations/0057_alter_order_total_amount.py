# Generated by Django 5.0.6 on 2024-09-11 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0056_remove_order_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
