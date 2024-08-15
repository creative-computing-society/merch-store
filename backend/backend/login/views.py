from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout

from .serializers import UserSerializer
from .models import CustomUser as User

from dotenv import load_dotenv
load_dotenv()


class LoginTokenView(APIView):
    def post(self, request):
        sso_token = request.data.get('token')
        if not sso_token:
            return Response({'error': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, sso_token=sso_token)
        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        print(f"User {user} logged in successfully with ID: {user.pk}")

        token, _ = Token.objects.get_or_create(user=user)

        serializer = UserSerializer(user)
        user.save()
        
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        token =Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
