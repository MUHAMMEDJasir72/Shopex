# Generated by Django 5.0.6 on 2024-09-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ad_min', '0035_alter_salesreport_overall_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesreport',
            name='overall_amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salesreport',
            name='overall_discount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='salesreport',
            name='sales_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
