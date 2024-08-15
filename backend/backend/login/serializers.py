from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'phone_no', 'position', 'is_member', 'profilePic')
