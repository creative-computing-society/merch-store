from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.AllOrders.as_view()),
    path('place/', views.Checkout.as_view())
]
