# Generated by Django 5.0.6 on 2024-09-04 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0020_alter_coupon_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_offer_percentage', models.IntegerField()),
            ],
        ),
    ]
