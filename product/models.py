from django.db import models
from django.contrib.postgres.fields import ArrayField
from login.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    
    is_name_required = models.BooleanField(default=False)
    is_size_required = models.BooleanField(default=False)
    accept_orders = models.BooleanField(default=True)
    
    description = models.TextField(null=True, blank=True, default=None)
    
    for_user_positions = ArrayField(base_field=models.CharField(max_length=2), size=4, default=list, help_text="comma separated list: MB - member, CR - Core, JS - Joint Sec, GS - Gen Sec. Ex: GS,JS,CR")

    image_url1 = models.URLField(max_length=5000, null=True, blank=True, default=None)
    image_url2 = models.URLField(max_length=5000, null=True, blank=True, default=None)

    size_chart_url = models.URLField(max_length=5000, null=True, default=None, blank=True)
    
    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    printing_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    size =  models.CharField(max_length=5, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.user.email}_{self.product.name}"
    