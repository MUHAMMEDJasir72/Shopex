# Generated by Django 5.0.6 on 2024-09-11 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0027_product_brand_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='final_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
