# order/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("order/all/", AllOrders.as_view(), name="all_orders"),
    path("order/<int:order_id>/", OrderView.as_view(), name="order_view"),
    path("order/place/", Checkout.as_view(), name="place_order"),
    path("order/apply-discount/", ApplyDiscount.as_view(), name="apply_discount"),
    # path("payment/success/", PaymentSuccessView.as_view(), name="payment_success"),
    # path("payment/failure/", PaymentFailureView.as_view(), name="payment_failure"),
    # path("payment/callback/", PhonePeCallbackView.as_view(), name="phonepe_callback"),
    path(
        "payment_completed/verify/", PaymentVerifyView.as_view(), name="payment_verfiy"
    ),
    path(
        "payment_completed/result/", PaymentResultView.as_view(), name="payment_result"
    ),
    path("payment/<str:order_id>/", PaymentView.as_view(), name="payment_checkout"),
]
