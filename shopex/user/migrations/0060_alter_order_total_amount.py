# Generated by Django 5.0.6 on 2024-09-11 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0059_orderitem_offer_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(),
        ),
    ]
