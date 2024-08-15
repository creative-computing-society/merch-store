from django import forms
from discounts.models import DiscountCode
from products.models import Product


class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = [
            "code",
            "discount_percentage",
            "max_uses",
            "expiry_date",
            "for_user_positions",
            "custom",
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "image1",
        ]
