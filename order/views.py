from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from .models import Order,OrderItem
from product.models import CartItem
from .serializers import OrderSerializer

from datetime import datetime
import string, random

allowed_extensions = ['jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'png', 'heic']

# Create your views here.

class AllOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = Order.objects.filter(user=user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        user = request.user
        order = Order.objects.filter(id=order_id, user=user).first()
        if order is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class initiateOrder(APIView):
    def get(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if cart_items.count()==0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        amount = 0.00

        for item in cart_items:
            if item.product.accept_orders==False or item.product.is_visible==False:
                item.delete()
            else:
                amount += float(item.product.price)
        
        data = {
            'amount': amount,
            'upi_id': settings.UPI_ID,
            'wallet': settings.WALLET,
            'qr_link': settings.QR_LINK
        }
        
        return Response(data, status=status.HTTP_200_OK)


def generateOrderId():
    flag = "".join(random.choice(string.ascii_letters) for _ in range(6))
    time = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"ccs_{time}_{flag}"

class placeOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        screenshot = request.data.get('screenshot')

        if screenshot is None:
            return Response({'error': 'Screenshot file missing'}, status=status.HTTP_400_BAD_REQUEST)

        if screenshot.name.split('.')[-1] not in allowed_extensions:
            return Response({'error': 'Invalid file type. Allowed file types are png, jpg and heic'}, status=status.HTTP_400_BAD_REQUEST)

        if screenshot.size>11534400:
            return Response({'error': 'Maximum file size is 10MB'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(user=user)

        if cart_items.count()==0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order_id = generateOrderId()
        while(Order.objects.filter(id=order_id).exists()):
            order_id = generateOrderId()
        order = Order(id=order_id, user=user, amount='0', screenshot=screenshot)
        order.save()

        amount = 0.00

        for item in cart_items:
            amount += float(item.product.price)
            order_item = OrderItem(order=order, product=item.product, printing_name=item.printing_name, size=item.size, image_url=item.image_url)
            order_item.save()
        
        order.amount = str(amount)
        order.save()
        
        for item in cart_items:
            item.delete()

        return Response(status=status.HTTP_200_OK)
