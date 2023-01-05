from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('change-password/', views.ChangePassword.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('user/', views.UserDetails.as_view())
]
