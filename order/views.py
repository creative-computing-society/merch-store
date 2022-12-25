from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order,OrderItem
from product.models import CartItem
from .serializers import OrderSerializer

from datetime import datetime
import string, random

# Create your views here.

class AllOrders(APIView):
    def get(self, request):
        user = request.user
        queryset = Order.objects.filter(user=user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def generateOrderId():
    flag = "".join(random.choice(string.ascii_letters) for _ in range(6))
    time = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"ccs_{time}#{flag}"

class Checkout(APIView):
    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if cart_items.count()==0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order_id = generateOrderId()
        while(Order.objects.filter(id=order_id).exists()):
            order_id = generateOrderId()
        order = Order(id=order_id, user=user, amount='0')
        order.save()

        amount = 0

        for item in cart_items:
            prev_ordered = OrderItem.objects.filter(product=item.product, order__user=user).exists()
            if prev_ordered:
                order.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
            amount += int(item.product.price)
            order_item = OrderItem(order=order, product=item.product, printing_name=item.printing_name, size=item.size)
            order_item.save()
        
        order.amount = str(amount)
        order.save()

        for item in cart_items:
            item.delete()
        
        return Response(status=status.HTTP_200_OK)

