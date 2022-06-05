# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from django.contrib.auth.models import User

# Django
from django.contrib.auth import (
    authenticate,
    password_validation
)


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""
    
    class Meta:
        """Meta class."""
        
        model = User
        fields = (
            'username',
            'first_name',
            'last_name'
        )


class UserLoginSerializer(serializers.Serializer):
    """
    User login serializer.
    Handle the login request data.
    """
    
    username = serializers.CharField(min_length=4, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)
    
    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        self.context['user'] = user
        return data
    
    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
    
    
class UserSignupSerializer(serializers.Serializer):
    """
    User signup serializer.
    Handle signup data validation and user/profile creation.
    """
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    
    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    
    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    
    def validate(self, data):
        """Check passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data
    
    
    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user