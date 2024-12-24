import hashlib
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
merchant_id = "PGTESTPAYUAT86"
salt_key = "96434309-7796-489d-8924-ab56988a6076"
salt_index = 1
env = "UAT"  # Change to "PROD" when you go live

# Base URLs for PhonePe API
BASE_URLS = {
    "UAT": "https://api-preprod.phonepe.com/apis/pg-sandbox",
    "PROD": "https://api.phonepe.com/apis/hermes"
}

# def generate_phonepe_signature(payload, salt_key, endpoint):
#     data = json.dumps(payload)
#     base64_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
#     signature_string = base64_data + endpoint + salt_key
#     return hashlib.sha256(signature_string.encode('utf-8')).hexdigest()

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
        ui_redirect_url = "http://localhost:3000/payment-status/"
        s2s_callback_url = "http://localhost:3377/payment/callback/"
        amount = int(order.updated_amount * 100)
        id_assigned_to_user_by_merchant = user.id

        payload = {
            "merchantId": merchant_id,
            "merchantTransactionId": unique_transaction_id,
            "merchantUserId": id_assigned_to_user_by_merchant,
            "amount": amount,
            "redirectUrl": ui_redirect_url,
            "redirectMode": "REDIRECT",
            "callbackUrl": s2s_callback_url,
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }

        json_payload = json.dumps(payload)
        base64_payload = base64.b64encode(json_payload.encode('utf-8')).decode('utf-8')

        endpoint = "/pg/v1/pay"
        signature_string = base64_payload + endpoint + salt_key
        checksum = hashlib.sha256(signature_string.encode('utf-8')).hexdigest()
        x_verify = f"{checksum}###{salt_index}"

        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": x_verify
        }

        base_url = BASE_URLS[env]
        max_retries = 5
        retry_delay = 1  # Initial delay in seconds

        for attempt in range(max_retries):
            response = requests.post(
                f"{base_url}{endpoint}",
                json={"request": base64_payload},
                headers=headers
            )

            # Log the payload and response for debugging
            print("Payload:", payload)
            print("Base64 Payload:", base64_payload)
            print("X-VERIFY Header:", x_verify)
            print("Response Status Code:", response.status_code)
            print("Response Content:", response.content)

            if response.status_code == 200:
                pay_page_url = response.json().get("data", {}).get("instrumentResponse", {}).get("redirectInfo", {}).get("url")
                Payment.objects.create(
                    order=order,
                    transaction_id=unique_transaction_id,
                    paid_amount=order.updated_amount,
                    status="pending",
                )
                return Response({"pay_page_url": pay_page_url}, status=status.HTTP_200_OK)
            elif response.status_code == 429:
                # Too many requests, wait and retry
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                break

        return Response(
            {"detail": "Payment initiation failed."},
            status=status.HTTP_400_BAD_REQUEST
        )
            

# class PaymentSuccessView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = [AllowAny]

#     def post(self, request):
#         txnid = request.data.get("txnid")
#         status = request.data.get("status")
#         payment_id = request.data.get("mihpayid")
#         reason = request.data.get("field9")

#         try:
#             payment = Payment.objects.get(transaction_id=txnid)
#             payment.status = status
#             payment.payment_id = payment_id
#             payment.reason = reason
#             payment.save()

#             if status == "success":
#                 payment.order.is_verified = True
#                 payment.order.save()

#                 # Increment the discount code uses if present
#                 if payment.order.discount_code:
#                     payment.order.discount_code.uses += 1
#                     payment.order.discount_code.save()

#                 # Remove items from the cart
#                 CartItem.objects.filter(user=payment.order.user).delete()

#                 order_items = OrderItem.objects.filter(order=payment.order).all()
#                 prod_list = []
#                 for item in order_items:
#                     prod_list.append(
#                         {
#                             "name": item.product.name,
#                             "quantity": item.quantity,
#                         }
#                     )

#                 # Generate and save QR code
#                 qr_data = generate_qr_code(payment.order)

#                 send_order_success_email_async(
#                     payment.transaction_id,
#                     payment.order.updated_amount,
#                     prod_list,
#                     payment.order.user.name,
#                     qr_data,
#                     payment.order.user.email,
#                 )

#                 redirect_url = f"http://localhost:3000/payment-status/{txnid}"
#                 # redirect_url = f"https://merch.ccstiet.com/payment-status/{txnid}"
#                 return redirect(redirect_url)

#         except Payment.DoesNotExist:
#             return Response(
#                 {"detail": "Payment record not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )


# class PaymentFailureView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = [AllowAny]

#     def post(self, request):
#         txnid = request.data.get("txnid")
#         status = request.data.get("status")
#         payment_id = request.data.get("mihpayid")
#         reason = request.data.get("field9")

#         try:
#             payment = Payment.objects.get(transaction_id=txnid)
#             payment.status = status
#             payment.payment_id = payment_id
#             payment.reason = reason
#             payment.save()

#             if status == "failure":
#                 payment.order.is_verified = False
#                 payment.order.save()
#                 redirect_url = f"http://localhost:3000/payment-status/{txnid}"
#                 # redirect_url = f"https://merch.ccstiet.com/payment-status/{txnid}"
#                 return redirect(redirect_url)

#         except Payment.DoesNotExist:
#             return Response(
#                 {"detail": "Payment record not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )


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
            

class PhonePeCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            base64_response = request.data.get("response")
            x_verify = request.headers.get("X-VERIFY")

            # Log the callback request for debugging
            print("Callback Base64 Response:", base64_response)
            print("Callback X-VERIFY Header:", x_verify)

            # Decode the base64 response
            decoded_response = base64.b64decode(base64_response).decode('utf-8')
            response_data = json.loads(decoded_response)

            # Log the decoded response for debugging
            print("Decoded Callback Response:", response_data)

            # Validate the checksum
            calculated_checksum = hashlib.sha256((base64_response + salt_key).encode('utf-8')).hexdigest()
            expected_x_verify = f"{calculated_checksum}###{salt_index}"
            if x_verify != expected_x_verify:
                return Response({"detail": "Invalid checksum."}, status=status.HTTP_400_BAD_REQUEST)

            # Extract payment details
            data = response_data.get("data")
            merchant_transaction_id = data.get("merchantTransactionId")
            status = data.get("state")
            transaction_id = data.get("transactionId")
            amount = data.get("amount")

            # Update payment record
            try:
                payment = Payment.objects.get(transaction_id=merchant_transaction_id)
                payment.payment_id = transaction_id
                payment.paid_amount = amount
                payment.status = status
                payment.save()

                if status == "COMPLETED":
                    payment.order.is_verified = True
                else:
                    payment.order.is_verified = False
                payment.order.save()

                return Response({"detail": "Payment record updated successfully."}, status=status.HTTP_200_OK)

            except Payment.DoesNotExist:
                return Response({"detail": "Payment record not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Log the exception for debugging
            print("Exception in PhonePeCallbackView:", str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)