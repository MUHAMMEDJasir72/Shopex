# Generated by Django 5.0.6 on 2024-09-05 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0024_product_product_offer'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_offer_percentage', models.IntegerField()),
            ],
        ),
    ]
