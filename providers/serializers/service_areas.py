# Django REST Framework
from rest_framework import serializers

# Models
from providers.models.service_areas import ServiceArea
from providers.models.providers import Provider


class ServiceAreaSerializer(serializers.ModelSerializer):
    """
    Service Area serializer.
    """
    class Meta:
        model = ServiceArea
        fields = ('name', 'price', 'area')
    
    def validate(self, data):
        """Add the given provider to the serializer context."""
        try:
            provider = Provider.objects.get(id=self.context['provider'])
        except Provider.DoesNotExist:
            raise serializers.ValidationError('This provider does not exists.')
                
        self.context['provider'] = provider
        
        return data
                            
    def validate_area(self, data):
        """
        Validates the 'area' data of the Service Area
        objects and restructures it to obtain a JSON with
        ordered geographic information.
        """
        if not isinstance(data, list):
            raise serializers.ValidationError('This field should be a list of coordinates.')
        
        latitude_list = []
        longitude_list = []

        for item in data:
            if not isinstance(item, list):
                raise serializers.ValidationError('This field should be a list of coordinates.')
            
            if not len(item)==2:
                raise serializers.ValidationError('Coordinates must have 2 values (X, Y).')
            
            for count, i in enumerate(item):
                if not isinstance(i, float):
                    raise serializers.ValidationError('A coordinate must be a float value.')
                
                if count==0:
                    latitude_list.append(i)
                else:
                    longitude_list.append(i)
        
        new_data = {
            'polygon': data,
            'lt_max': max(latitude_list),
            'lt_min': min(latitude_list),
            'lg_max': max(longitude_list),
            'lg_min': min(longitude_list)
        }

        return new_data
    
    def create(self, data):
        """Create a Service Area object."""
        service_area = ServiceArea.objects.create(**data, provider=self.context['provider'])
        return service_area