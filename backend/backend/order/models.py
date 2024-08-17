from decimal import Decimal
from django.db import models
from products.models import Product
from login.models import CustomUser as User
from discounts.models import DiscountCode

class ThreeCharAutoField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add:
            last_id = model_instance.__class__.objects.all().values_list('id', flat=True).last()
            if last_id:
                last_id = last_id.split('_')[1]
                last_id = int(last_id) + 1
            else:
                last_id = 1

            value = 'order_'+str(last_id)
            setattr(model_instance, self.attname, value)
        return super().pre_save(model_instance, add)

class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)  # True if the payment of this order is verfied
    mail_added = models.BooleanField(default=False)
    discount_code = models.ForeignKey(DiscountCode, null=True, blank=True, on_delete=models.SET_NULL)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qr_code_data = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def calculated_total_amount(self):
        total = sum(Decimal(item.product.price * item.quantity) for item in self.order_items.all())
        if self.discount_code and self.discount_code.is_valid():
            discount = total * (Decimal(self.discount_code.discount_percentage) / Decimal(100))
            total -= discount
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='order_items')
    printing_name = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=5, null=True, blank=True)
    image_url = models.URLField(max_length=5000, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order.id}_{self.product.name}"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100, unique=True) # Our transaction ID
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)  # 'success', 'failure', 'pending'
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True, unique=True)  # Payment gateway's payment ID
    reason = models.TextField(null=True, blank=True)  # Reason for failure
    

    def __str__(self):
        return f"Payment for Order {self.order.id}"
