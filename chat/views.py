from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserGetSerializer, ChatSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from account.models import User

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        user_obs = User.objects.exclude(id=request.user.id)
        serializer = UserGetSerializer(user_obs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat(request, chat_id):
    try:
        sender = request.user
        receiver = User.objects.get(id=chat_id)
        
        chat = Chat.objects.filter(sender=sender, receiver=receiver) | Chat.objects.filter(sender=receiver, receiver=sender)
        serializer = ChatSerializer(chat, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Receiver user does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Chat.DoesNotExist:
        return Response({"error": "Chat does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reciver(request, chat_id):
    try:
        if chat_id == 0:
            return Response(None , status=status.HTTP_400_BAD_REQUEST)
        receiver = User.objects.get(id=chat_id)
        serializer = UserGetSerializer(receiver)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Receiver user does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sender(request):
    try:
        sender = request.user
        serializer = UserGetSerializer(sender)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
