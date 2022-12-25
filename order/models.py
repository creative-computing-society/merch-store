from django.db import models

from product.models import Product
from login.models import User

# Create your models here.

class Order(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=10)

    def __str__(self):
        return self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='order_items')

    printing_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    size = models.CharField(max_length=5, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.order.id }_{self.product.name}"
