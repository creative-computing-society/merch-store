# Generated by Django 4.1.4 on 2022-12-31 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_rename_is_paid_order_is_verified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart_restored',
            field=models.BooleanField(default=False),
        ),
    ]
