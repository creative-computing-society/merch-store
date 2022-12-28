from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    position_text = serializers.SerializerMethodField()

    def get_position_text(self, obj):
        if obj.position=='GS':
            return "General Secretary"
        if obj.position=='JS':
            return "Joint Secretary"
        if obj.position=='CR':
            return "Core Member"
        return "Member"

    class Meta:
        model = User
        fields = ('name', 'email', 'phone_no', 'position_text')
