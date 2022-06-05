# Django REST Framework
from rest_framework import viewsets, mixins

# Permissions
from providers.permissions.providers_permissions import IsProviderOwner
from rest_framework.permissions import IsAuthenticated

# Models
from providers.models.service_areas import ServiceArea

# Serializers
from providers.serializers.service_areas import ServiceAreaSerializer


class ServiceAreaViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """Service Area view set."""
    
    model = ServiceArea
    serializer_class = ServiceAreaSerializer
    permission_classes = [IsAuthenticated, IsProviderOwner] 

    def get_queryset(self):
        """Return a Service Area queryset for a given provider."""
        provider_id = int(self.kwargs['provider_id'])
        queryset = self.model.objects.filter(provider__id=provider_id)
        return queryset
            
    def get_serializer_context(self):
        """Add provider id to serializer context."""
        context = super(ServiceAreaViewSet, self).get_serializer_context()
        context['provider'] = int(self.kwargs['provider_id'])
        return context