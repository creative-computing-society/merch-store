from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'printing_name', 'size', 'image_url']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_time(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M")
    
    def get_status(self, obj):
        if obj.is_verified is None:
            return "Pending"
        if obj.is_verified:
            return "Success"
        return "Failed"

    class Meta:
        model = Order
        fields = ['id', 'amount', 'time', 'status', 'order_items']
