# Generated by Django 5.0.6 on 2024-08-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_orderitem_order_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order_item_status',
            field=models.BooleanField(default=True),
        ),
    ]
