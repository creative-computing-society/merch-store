from django.urls import path
from . import views

urlpatterns = [
    path('product/all/', views.AllProductsView.as_view()),
    path('product/<int:product_id>/', views.ProductView.as_view()),
    path('cart/add/', views.AddToCart.as_view()),
    path('cart/view/', views.ViewCart.as_view()),
    path('cart/delete/', views.RemoveFromCart.as_view()),
    path('cart/update/', views.UpdateCart.as_view()),
]