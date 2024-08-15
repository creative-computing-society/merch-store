from django.urls import path
from django.contrib import admin
from .views import LoginTokenView, LogoutView, UserDetails

urlpatterns = [
    path('login/', LoginTokenView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserDetails.as_view()),
]
