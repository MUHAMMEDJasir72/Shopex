# Generated by Django 5.0.6 on 2024-08-21 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_addresses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addresses',
            old_name='mobail_number',
            new_name='mobil_number',
        ),
    ]
