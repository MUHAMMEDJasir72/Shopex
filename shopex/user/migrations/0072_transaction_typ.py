# Generated by Django 5.0.6 on 2024-09-27 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0071_alter_couponused_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='typ',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
