from rest_framework import serializers
from .models import Product, CartItem
from order.models import OrderItem

class ProductSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        user = self.context.get('user')
        if user is None or user.is_anonymous:
            return "forbidden"
        if not obj.accept_orders:
            return "nostock"
        # if OrderItem.objects.filter(product=obj, order__user=user).exclude(order__is_verified=False).exists():
        #     return "ordered"
        if CartItem.objects.filter(product=obj, user=user).exists():
            return "incart"
        return "allowed"

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'max_quantity', 'is_name_required', 'is_size_required', 'is_image_required', 'image1', 'image2', 'status', 'size_chart_image']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'printing_name', 'size', 'image_url']

