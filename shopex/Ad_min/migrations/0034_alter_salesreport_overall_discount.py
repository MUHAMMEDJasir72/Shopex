# Generated by Django 5.0.6 on 2024-09-12 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0033_alter_salesreport_overall_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesreport',
            name='overall_discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
