# Django REST Framework
from rest_framework import serializers

# Models
from providers.models.providers import Provider


class ProviderSerializer(serializers.ModelSerializer):
    """
    Provider serializer.
    Handle all data from Provider objects, in order to validate,
    update, create, and show information about providers.
    """
    
    class Meta:
        """Meta class."""
        
        model = Provider
        fields = ('name', 'email', 'phone_number', 'language', 'currency')
        
    def create(self, data):
        """Create a Provider object for a given user."""
        provider = Provider.objects.create(**data, user=self.context['user'])
        return provider