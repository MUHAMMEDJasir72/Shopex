# Generated by Django 5.0.6 on 2024-09-09 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0027_product_brand_offer'),
        ('user', '0044_remove_wishlist_products_wishlist_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Ad_min.productvariant'),
            preserve_default=False,
        ),
    ]
