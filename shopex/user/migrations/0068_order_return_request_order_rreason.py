# Generated by Django 5.0.6 on 2024-09-26 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0067_couponused_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='return_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='rreason',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
