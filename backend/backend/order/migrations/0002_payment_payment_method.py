# Generated by Django 4.2.11 on 2024-08-17 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.JSONField(blank=True, null=True),
        ),
    ]