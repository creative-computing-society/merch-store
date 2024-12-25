import hashlib
import logging
import time
import json
import base64
import requests
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, PaymentSerializer
from .utils import generate_qr_code
from discounts.models import DiscountCode
from products.models import CartItem
from requests.exceptions import HTTPError

from .tasks import send_order_success_email_async
from datetime import datetime, timedelta
import pytz
import random

# Test keys
merchant_id = settings.PHONEPE_MERCHANT_ID
salt_key = settings.PHONEPE_SALT_KEY
salt_index = 1
env = "PROD"  # Change to "PROD" when you go live

# Base URLs for PhonePe API
BASE_URLS = {
    "UAT": "https://api-preprod.phonepe.com/apis/pg-sandbox",
    "PROD": "https://api.phonepe.com/apis/hermes",
}


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
                id=f"ccs_order_{id_num}",
                user=user,
                updated_amount=updated_amount,
                total_amount=total_amount,
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

        unique_transaction_id = str(order.id) + str(int(time.time() * 1000))
        # ui_redirect_url = "http://localhost:8000/payment_completed/verify/"
        ui_redirect_url = f"{settings.PHONEPE_RETURN_URL}{unique_transaction_id}/"
        s2s_callback_url = settings.PHONEPE_CALLBACK_URL  # Use HTTPS

        amount = int(order.updated_amount * 100)
        id_assigned_to_user_by_merchant = user.id

        payload = {
            "merchantId": merchant_id,
            "merchantTransactionId": unique_transaction_id,
            "merchantUserId": id_assigned_to_user_by_merchant,
            "amount": amount,
            "redirectUrl": ui_redirect_url,
            "redirectMode": "REDIRECT",  # Uncomment this line for S2S callback
            # "redirectMode": "POST",
            "callbackUrl": s2s_callback_url,  # Ensure correct case
            "paymentInstrument": {"type": "PAY_PAGE"},
        }

        json_payload = json.dumps(payload)
        base64_payload = base64.b64encode(json_payload.encode("utf-8")).decode("utf-8")

        endpoint = "/pg/v1/pay"
        signature_string = base64_payload + endpoint + salt_key
        checksum = hashlib.sha256(signature_string.encode("utf-8")).hexdigest()
        x_verify = f"{checksum}###{salt_index}"

        headers = {"Content-Type": "application/json", "X-VERIFY": x_verify}

        base_url = BASE_URLS[env]
        max_retries = 5
        retry_delay = 1  # Initial delay in seconds

        for attempt in range(max_retries):
            response = requests.post(
                f"{base_url}{endpoint}",
                json={"request": base64_payload},
                headers=headers,
            )

            if response.status_code == 200:
                pay_page_url = (
                    response.json()
                    .get("data", {})
                    .get("instrumentResponse", {})
                    .get("redirectInfo", {})
                    .get("url")
                )
                Payment.objects.create(
                    order=order,
                    transaction_id=unique_transaction_id,
                    paid_amount=order.updated_amount,
                    status="pending",
                )
                return Response(
                    {"pay_page_url": pay_page_url}, status=status.HTTP_200_OK
                )
            elif response.status_code == 429:
                # Too many requests, wait and retry
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                break

        return Response(
            {"detail": "Payment initiation failed."}, status=status.HTTP_400_BAD_REQUEST
        )


# Working with POST UI CALLBACK, SHUDNT BE USED IN PROD
# class PaymentVerifyView(APIView):
#     def post(self, request):
#         data = request.data
#         merchant_transaction_id = data.get("transactionId")
#         payment = Payment.objects.get(transaction_id=merchant_transaction_id)
#         payment.status = data.get("code")
#         payment.payment_id = data.get("providerReferenceId")
#         payment.reason = data.get("code")
#         payment.save()
#         if data.get("code") == "PAYMENT_SUCCESS":
#             payment.order.is_verified = True
#             generate_qr_code(payment.order)
#             payment.order.save()
#             if payment.order.discount_code:
#                 payment.order.discount_code.uses += 1
#                 payment.order.discount_code.save()

#             CartItem.objects.filter(user=payment.order.user).delete()

#             order_items = OrderItem.objects.filter(order=payment.order).all()
#             prod_list = []
#             for item in order_items:
#                 prod_list.append(
#                     {
#                         "name": item.product.name,
#                         "quantity": item.quantity,
#                     }
#                 )
#         else:
#             payment.order.is_verified = False
#             payment.order.save()
#         return redirect(
#             f"http://localhost:3000/payment-status/{payment.transaction_id}"
#         )


# Correct code to use with REDIRECT and S2S callback
class PaymentVerifyView(APIView):
    def post(self, request):
        b64_payload = request.data.get("response")
        payload = json.loads(base64.b64decode(b64_payload).decode("utf-8"))

        if not payload:
            return Response(
                {"detail": "Invalid payload."}, status=status.HTTP_400_BAD_REQUEST
            )

        data = payload.get("data")
        merchant_transaction_id = data.get("merchantTransactionId")

        signature_string = (
            f"/pg/v1/status/{merchant_id}/{merchant_transaction_id}" + salt_key
        )
        checksum = hashlib.sha256(signature_string.encode("utf-8")).hexdigest()
        x_verify = f"{checksum}###{salt_index}"

        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": x_verify,
            "X-MERCHANT-ID": merchant_id,
        }
        response = requests.get(
            f"https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchant_id}/{merchant_transaction_id}",
            headers=headers,
        )

        if response.json().get("success") != True:
            return Response(
                {"detail": "Payment verification failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        resp_data = response.json()
        data2 = resp_data.get("data")
        if resp_data.get("code") != "PAYMENT_SUCCESS":
            return Response(
                {"detail": "Payment verification failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.get(transaction_id=merchant_transaction_id)
        payment.status = resp_data.get("code")
        payment.payment_id = data2.get("transactionId")
        payment.reason = data2.get("state")
        payment.save()

        if resp_data.get("code") == "PAYMENT_SUCCESS":

            payment.order.is_verified = True
            payment.order.save()
            if payment.order.discount_code:
                payment.order.discount_code.uses += 1
                payment.order.discount_code.save()

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

            qr_data = generate_qr_code(payment.order)
            send_order_success_email_async(
                payment.transaction_id,
                payment.order.updated_amount,
                prod_list,
                payment.order.user.name,
                qr_data,
                payment.order.user.email,
            )
            return Response(
                {"detail": "Payment successful."}, status=status.HTTP_200_OK
            )
        else:
            payment.order.is_verified = False
            payment.order.save()
            return Response({"detail": resp_data}, status=status.HTTP_400_BAD_REQUEST)


class PaymentResultView(APIView):
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
