# Generated by Django 5.0.6 on 2024-09-03 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0019_alter_productvariant_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='percentage',
            field=models.IntegerField(),
        ),
    ]
