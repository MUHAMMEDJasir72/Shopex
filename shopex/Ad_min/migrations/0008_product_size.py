# Generated by Django 5.0.6 on 2024-08-15 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0007_product_productsize'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
