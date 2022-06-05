# Django REST Framework
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, views
from rest_framework.decorators import action

# Permissions
from providers.permissions.providers_permissions import IsProviderOwner
from rest_framework.permissions import IsAuthenticated


# Serializers
from providers.serializers.providers import ProviderSerializer

# Models
from providers.models.providers import Provider
from providers.models.service_areas import ServiceArea

# Shapely
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class ProviderViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Provider view set."""
    
    model = Provider
    serializer_class = ProviderSerializer
    
    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]            
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            permissions.append(IsProviderOwner)
        return [permission() for permission in permissions]

    def get_queryset(self):
        """Return a Provider queryset of the request user."""
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset
            
    def get_serializer_context(self):
        """Add request user to serializer context."""
        context = super(ProviderViewSet, self).get_serializer_context()
        context['user'] = self.request.user
        return context
    

class ActiveProvidersAPIView(views.APIView):
    """Return a list of providers which works
    on an specific location. This location is defined
    by its latitude and longitude, received by parameters (URL)
    """
    
    model = ServiceArea
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        latitude = self.kwargs.get('lt', None)
        longitude = self.kwargs.get('lg', None)
        polygons_list = []

        if latitude and longitude:
            
            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except:
                error = {'error':"'lt' and 'lg' params should be formatted as float values."}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            point = Point(latitude, longitude)
            
            queryset = self.model.objects.filter(area__lg_max__gte=longitude,area__lg_min__lte=longitude,area__lt_max__gte=latitude,area__lt_min__lte=latitude)
            
            if queryset.exists():
                for service_area in queryset:
                    polygon = Polygon(service_area.area['polygon'])
                    if polygon.contains(point):
                        service_area_data = {
                            'name':service_area.name,
                            'provider_name':service_area.provider.name,
                            'price':service_area.price
                        }
                        polygons_list.append(service_area_data)
                
        return Response(polygons_list, status=status.HTTP_200_OK)