# Generated by Django 5.0.6 on 2024-08-15 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0008_product_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='product_type',
        ),
    ]
