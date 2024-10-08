# order/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("order/all/", AllOrders.as_view(), name="all_orders"),
    path("order/place/", Checkout.as_view(), name="place_order"),
    path("order/apply-discount/", ApplyDiscount.as_view(), name="apply_discount"),
    path('payment/verify/', PaymentVerifyView.as_view(), name='payment_verfiy'),
    path('payment/webhook/<str:order_id>/', PaymentWebhookView.as_view(), name='payment_webhook'),
    path('payment/<str:order_id>/', PaymentView.as_view(), name='payment_checkout'),
    path("order/<str:order_id>/", OrderView.as_view(), name="order_view"),
]
