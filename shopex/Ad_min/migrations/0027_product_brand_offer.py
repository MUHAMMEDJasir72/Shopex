# Generated by Django 5.0.6 on 2024-09-05 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0026_brandoffer_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand_offer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
