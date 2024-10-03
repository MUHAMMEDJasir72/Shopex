# Generated by Django 5.0.6 on 2024-08-15 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0009_rename_category_product_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productbrand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='Ad_min.brand'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=100),
        ),
    ]
