from rest_framework import serializers
from .models import Order, OrderItem, Payment
from discounts.models import DiscountCode
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['product', 'printing_name', 'size', 'image_url', 'quantity']

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['code', 'discount_percentage', 'max_uses', 'expiry_date', 'custom']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()
    discount_code = DiscountCodeSerializer(read_only=True)
    total_amount = serializers.SerializerMethodField()
    qr_code_data = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    
    def get_qr_code_data(self, obj):
        if obj.qr_code_data:
            return obj.qr_code_data
        return None
    
    def get_is_completed(self, obj):
        return obj.is_completed
    
    def get_created_at(self, obj):
        return obj.created_at.isoformat()
    
    def get_is_verified(self, obj):
        if obj.is_verified is None:
            return "Pending"
        if obj.is_verified:
            return "Verified"
        return "Not Verified"
    
    def get_total_amount(self, obj):
        return obj.total_amount

    class Meta:
        model = Order
        fields = ['id', 'updated_amount', 'created_at', 'is_verified', 'order_items', 'discount_code', 'total_amount','qr_code_data', 'is_completed']
        
class PaymentSerializer(serializers.ModelSerializer):
    qr_code_data = serializers.SerializerMethodField()
    
    def get_qr_code_data(self, obj):
        if obj.order.qr_code_data:
            return obj.order.qr_code_data
        return None
    
    class Meta:
        model = Payment
        fields = ['transaction_id', 'paid_amount', 'status', 'payment_date', 'payment_id', 'reason', 'qr_code_data']
