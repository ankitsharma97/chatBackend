from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from .tokenAuthentication import TokenAuthentication

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['name'] = account.name
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        data = {}
        if serializer.is_valid():
                print(serializer.validated_data)
                token = TokenAuthentication.generate_jwt(serializer.validated_data)
                data['response'] = 'successfully logged in.'
                data['token'] = token
                data['user'] = serializer.validated_data
                data['user_id'] = serializer.validated_data['id']
        else:
                data['response'] = 'Invalid credentials'
        print(data)
    else:
            data = serializer.errors

    return Response(data)
    
