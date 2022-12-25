from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'printing_name', 'size']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    time = serializers.SerializerMethodField()

    def get_time(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M")

    class Meta:
        model = Order
        fields = ['amount', 'time', 'order_items']
