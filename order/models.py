from django.db import models

from product.models import Product, CartItem
from login.models import User

# Create your models here.

def screenshot_file_path(obj, filename):
    return f"screenshots/{obj.user.email.split('@')[0]}_{filename}"

class Order(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=10)

    screenshot = models.ImageField(upload_to=screenshot_file_path, null=True, default=None)
    is_verified = models.BooleanField(null=True, default=None)

    cart_restored = models.BooleanField(default=False) #to check if cart restored in case of failed attemt
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.is_verified and not self.cart_restored:
            self.cart_restored = True
            order_items = self.order_items.all()
            for item in order_items:
                if not CartItem.objects.filter(user=self.user, product=item.product).exists():
                    cart_item = CartItem(user=self.user, product=item.product, printing_name=item.printing_name, size=item.size)
                    cart_item.save()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='order_items')

    printing_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    size = models.CharField(max_length=5, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.order.id }_{self.product.name}"
