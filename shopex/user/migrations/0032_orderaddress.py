# Generated by Django 5.0.6 on 2024-08-30 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_remove_orderitem_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('mobil_number', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('landmark', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
            ],
        ),
    ]
