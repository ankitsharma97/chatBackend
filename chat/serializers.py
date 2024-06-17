from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chat

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name')
        extra_kwargs = {'id': {'read_only': True}}

class ChatSerializer(serializers.ModelSerializer):
    sender = UserGetSerializer()
    receiver = UserGetSerializer()
    
    class Meta:
        model = Chat
        fields = '__all__'
