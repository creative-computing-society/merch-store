from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import string
import random

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_uses = models.IntegerField()
    expiry_date = models.DateTimeField()
    for_user_positions = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    custom = models.BooleanField(default=False)  # when True, code is entered by admin
    uses = models.IntegerField(default=0)

    def is_valid(self):
        if self.uses >= self.max_uses:
            return False
        if self.expiry_date < timezone.now():
            return False
        return True

    def save(self, *args, **kwargs):
        if not self.custom and not self.code:
            self.code = self.generate_random_code()
        super().save(*args, **kwargs)

    def generate_random_code(self):
        length = 10  # length of the code
        characters = string.ascii_uppercase + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    def __str__(self):
        return self.code
