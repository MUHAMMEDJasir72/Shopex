# Generated by Django 5.0.6 on 2024-09-09 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0049_wallet_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='created_at',
        ),
    ]
