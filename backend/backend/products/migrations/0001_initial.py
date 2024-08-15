# Generated by Django 4.2.11 on 2024-08-09 14:03

from decimal import Decimal
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('max_quantity', models.IntegerField(default=1)),
                ('is_name_required', models.BooleanField(default=False)),
                ('is_size_required', models.BooleanField(default=False)),
                ('is_image_required', models.BooleanField(default=False)),
                ('accept_orders', models.BooleanField(default=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('for_user_positions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, help_text='List of roles/positions that can view this product.', size=None)),
                ('image1', models.ImageField(blank=True, default=None, null=True, upload_to=products.models.productImageUploadPath)),
                ('image2', models.ImageField(blank=True, default=None, null=True, upload_to=products.models.productImageUploadPath)),
                ('size_chart_image', models.ImageField(blank=True, default=None, null=True, upload_to=products.models.productImageUploadPath)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5)),
                ('updated_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('printing_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('size', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('image_url', models.URLField(blank=True, default=None, max_length=5000, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
