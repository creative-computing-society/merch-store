from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.AllOrders.as_view()),
    path('initiate/', views.initiateOrder.as_view()),
    path('place/', views.placeOrder.as_view()),
    path('<slug:order_id>/', views.OrderView.as_view()),
]
