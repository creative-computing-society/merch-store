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

    mail_added = models.BooleanField(default=False) #to check if cart restored in case of failed attemt
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.mail_added and self.is_verified is not None:
            pending_email = PendingEmail(order=self)
            pending_email.save()
            if not self.is_verified:
                order_items = self.order_items.all()
                for item in order_items:
                    if not CartItem.objects.filter(user=self.user, product=item.product).exists():
                        cart_item = CartItem(user=self.user, product=item.product, printing_name=item.printing_name, size=item.size)
                        cart_item.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='order_items')

    printing_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    size = models.CharField(max_length=5, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.order.id }_{self.product.name}"


class PendingEmail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
