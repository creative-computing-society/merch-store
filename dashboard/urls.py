from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard),
    path('generate-orders-details/<int:id>/', views.ordersCSV, name='getOrdersDetails'),
    path('import-users/', views.importUsers, name='importUsers'),
    path('stop-orders/', views.stopOrders, name='stopOrders'),
]