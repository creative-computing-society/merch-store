import hashlib
import time
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db import transaction

from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, PaymentSerializer
from .utils import generate_qr_code
from discounts.models import DiscountCode
from products.models import CartItem

from .tasks import send_order_success_email_async

from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
from datetime import datetime, timedelta
import pytz
import random

Cashfree.XClientId = settings.CASHFREE_CLIENT_ID
Cashfree.XClientSecret = settings.CASHFREE_CLIENT_SECRET
Cashfree.XEnvironment = Cashfree.PRODUCTION
x_api_version = "2023-08-01"


def generateHash(params, salt):
    hashString = (
        params["key"]
        + "|"
        + params["txnid"]
        + "|"
        + params["amount"]
        + "|"
        + params["productinfo"]
        + "|"
        + params["firstname"]
        + "|"
        + params["email"]
        + "|"
        + params.get("udf1", "")
        + "|"
        + params.get("udf2", "")
        + "|"
        + params.get("udf3", "")
        + "|"
        + params.get("udf4", "")
        + "|"
        + params.get("udf5", "")
        + "||||||"
        + salt
    )
    return hashlib.sha512(hashString.encode("utf-8")).hexdigest().lower()


class AllOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = Order.objects.filter(user=user, is_verified=True)
        if not queryset.exists():
            return Response(
                {"detail": "No orders found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(queryset, many=True, context={"user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        user = request.user
        order = Order.objects.filter(id=order_id, user=user).first()
        if order is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(order, context={"user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplyDiscount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        discount_code = request.data.get("discount_code", None)

        if not discount_code:
            return Response(
                {"detail": "Discount code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response(
                {"detail": "No items in cart."}, status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        if discount_code == "NO_DISCOUNT":
            return Response(
                {
                    "total_amount": total_amount,
                    "discount_percentage": 0,
                    "updated_amount": total_amount,
                },
                status=status.HTTP_200_OK,
            )

        try:
            discount = DiscountCode.objects.get(code=discount_code)
            if discount.is_valid() and user.position in discount.for_user_positions:
                discount_percentage = discount.discount_percentage
                if discount_percentage == 100:
                    return Response(
                        {
                            "total_amount": float(total_amount),
                            "discount_percentage": float(discount_percentage),
                            "updated_amount": 1.00,
                        },
                        status=status.HTTP_200_OK,
                    )
                updated_amount = (total_amount) - (total_amount) * (
                    discount_percentage / 100
                )
                return Response(
                    {
                        "total_amount": float(total_amount),
                        "discount_percentage": float(discount_percentage),
                        "updated_amount": float(updated_amount),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Invalid or expired discount code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except DiscountCode.DoesNotExist:
            return Response(
                {"detail": "Discount code does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response(
                {"detail": "No items in cart."}, status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        updated_amount = total_amount

        discount_code = request.data.get("discount_code")

        if discount_code:
            try:
                discount = DiscountCode.objects.get(code=discount_code)
                if discount.is_valid() and user.position in discount.for_user_positions:
                    discount_percentage = discount.discount_percentage
                    if discount_percentage == 100:
                        updated_amount = 1.00
                    else:
                        updated_amount = total_amount - total_amount * (
                            discount_percentage / 100
                        )
                else:
                    return Response(
                        {"detail": "Invalid or expired discount code."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except DiscountCode.DoesNotExist:
                return Response(
                    {"detail": "Discount code does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        with transaction.atomic():
            id_num = random.randint(100000, 999999)
            while Order.objects.filter(id=f"ccs_order_{id_num}").exists():
                id_num = random.randint(100000, 999999)
            order = Order.objects.create(
                id=f"ccs_order_{id_num}",user=user, updated_amount=updated_amount, total_amount=total_amount
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    printing_name=item.printing_name,
                    size=item.size,
                    image_url=item.image_url,
                    quantity=item.quantity,
                )

            if discount_code:
                order.discount_code = discount
                order.save()

        serializer = OrderSerializer(order, context={"request": request})
        return Response(
            {
                "order": serializer.data,
                "total_amount": float(total_amount),
                "updated_amount": float(updated_amount),
                "discount_percentage": float(
                    discount.discount_percentage if discount_code else 0
                ),
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        user = request.user
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )

        amount = "{:.2f}".format(float(order.updated_amount))
        productinfo = str(order.id)
        firstname = str(user.name.split()[0] if " " in user.name else user.name)
        email = str(user.email)
        phone = str(user.phone_no)
        
        expiry_time = (datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(minutes=20)).isoformat()

        customerDetails = CustomerDetails(customer_id=str(user.id), customer_phone=phone)
        customerDetails.customer_name = firstname
        customerDetails.customer_email = email

        createOrderRequest = CreateOrderRequest(order_id=str(order_id), order_amount=float(amount), order_currency="INR", customer_details=customerDetails)

        orderMeta = OrderMeta()
        orderMeta.return_url = f"https://merch.ccstiet.com/payment-status/{order_id}/"
        orderMeta.notify_url = f"https://api.merch.ccstiet.com/payment/webhook/{order_id}/"
        orderMeta.payment_methods = "cc,dc,upi"
        createOrderRequest.order_meta = orderMeta
        createOrderRequest.order_expiry_time = expiry_time

        try:
            api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
            api_response = api_response.data
        except Exception as e:
            print(e)
            return Response(
                {"detail": "Order creation failed at cashfree"}, status=status.HTTP_404_NOT_FOUND
            )

        payload = {
            'payment_session_id': api_response.payment_session_id,
        }

        Payment.objects.create(
            order=order,
            transaction_id=order_id,
            paid_amount=order.updated_amount,
            status="pending",
        )

        return Response(payload, status=status.HTTP_200_OK)


def payment_success(payment):
    payment.order.is_verified = True
    payment.order.save()
    payment.status = "success"
    payment.save()

    # Increment the discount code uses if present
    if payment.order.discount_code:
        payment.order.discount_code.uses += 1
        payment.order.discount_code.save()

    # Remove items from the cart
    CartItem.objects.filter(user=payment.order.user).delete()

    order_items = OrderItem.objects.filter(order=payment.order).all()
    prod_list = []
    for item in order_items:
        prod_list.append(
            {
                "name": item.product.name,
                "quantity": item.quantity,
            }
        )

    # Generate and save QR code
    qr_data = generate_qr_code(payment.order)

    send_order_success_email_async(
        payment.transaction_id,
        payment.order.updated_amount,
        prod_list,
        payment.order.user.name,
        qr_data,
        payment.order.user.email,
    )

    # redirect_url = f"http://localhost:3000/payment-status/{txnid}"
    redirect_url = f"https://merch.ccstiet.com/payment-status/{payment.transaction_id}"
    return redirect(redirect_url)


def payment_failure(payment):
    payment.status = "failure"
    payment.save()

    if status == "failure":
        payment.order.is_verified = False
        payment.order.save()
        # redirect_url = f"http://localhost:3000/payment-status/{txnid}"
        redirect_url = f"https://merch.ccstiet.com/payment-status/{payment.transaction_id}"
        return redirect(redirect_url)


class PaymentWebhookView(APIView):
    def post(self, request, order_id):
        try:
            api_response = Cashfree().PGOrderFetchPayments(x_api_version, str(order_id), None)
            api_response = api_response.data[0] if api_response else None
            print(api_response)
        except:
            return Response(
                {"detail": "Payment record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        if api_response and api_response.payment_status == 'SUCCESS':
            payment = Payment.objects.get(transaction_id=order_id)
            payment_success(payment)
        else:
            payment = Payment.objects.get(transaction_id=order_id)
            payment_failure(payment)

        return Response(status=status.HTTP_200_OK)


class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        txnid = request.data.get("txnid")
        user = request.user

        try:
            payment = Payment.objects.get(transaction_id=txnid)
            if payment.order.user == user:
                serializer = PaymentSerializer(payment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "You do not have permission to view this payment."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
