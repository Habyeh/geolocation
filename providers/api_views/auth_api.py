# Django REST Framework
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny

# Serializers
from utils.serializers import (
    UserLoginSerializer,
    UserSignupSerializer,
    UserSerializer
)


class UserViewSet(viewsets.GenericViewSet):
    """Handle user's sign-up, login."""
    
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            "user": UserSerializer(user).data,
            "token": token
        }
        return Response(data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)