# Generated by Django 5.0.6 on 2024-08-23 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0012_product_status'),
        ('user', '0011_remove_cart_variant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.AddField(
            model_name='cart',
            name='product_variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='Ad_min.productvariant'),
            preserve_default=False,
        ),
    ]
