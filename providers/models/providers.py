# Django
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Utilities
from utils.models import BaseModel


class Provider(BaseModel):
    """Provider model.
    
    Entity that stores information of a transportation supplier
    which works in a specific area.
    """
    
    LANGUAGES = (
        ('en', 'English'),
        ('es', 'Spanish'),
        ('ja', 'Japanese'),
        ('de', 'German'),
        ('fr', 'French'),    
    )
    
    ALLOWED_CURRENCIES = (
        ('USD', 'U.S. Dollar'),
        ('EUR', 'European Euro'),
        ('JPY', 'Japanese Yen'),
        ('GBP', 'British Pound'),
        ('CHF', 'Swiss Franc'),
        ('CAD', 'Canadian Dollar')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50)
    
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )
    
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
        
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        error_messages={
            'invalid_choice': 'This language is not an option.'
        }
    )
    
    currency = models.CharField(
        max_length=3,
        choices=ALLOWED_CURRENCIES,
        error_messages={
            'invalid_choice': 'This currency is not allowed.'
        }
    )
    
    def __str__(self):
        """Return provider's name."""
        
        return self.name