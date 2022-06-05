# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Django
from django.urls import reverse

# Models
from django.contrib.auth.models import User
from providers.models.providers import Provider
from providers.models.service_areas import ServiceArea

# Serializers
from providers.serializers.service_areas import ServiceAreaSerializer


class ServiceAreaAPITestCase(APITestCase):
    """Test Service Area's Viewset CRUD."""
    
    def setUp(self):
        self.user_data = {
            'username': 'username',
            'password': '$010203*',
            'first_name': 'first_name',
            'last_name': 'last_name'
        }
        self.provider_creation_data = {
            "name": "aprovidername",
            "email":"provideremail@ff.io",
            "language":"en",
            "currency": "USD",
            "phone_number": "+584120195481"
        }
        self.service_area_creation_data = {
            "name": "Area151",
            "price": 10.00,
            "area": [
                [0.0, 0.0],
                [0.0, 1.0],
                [1.0, 1.0],
                [1.0, 0.0]
            ]
        }
        
        self.user = User.objects.create(**self.user_data)
        self.provider = Provider.objects.create(
            **self.provider_creation_data,
            user=self.user
        )
        self.service_area = ServiceArea.objects.create(
            **self.service_area_creation_data,
            provider=self.provider
        )
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
    def test_service_area_validation(self):
        """Test Service Area validation process."""
        
        data = {
            "name": "Area",
            "price": 10,
            "area": 1
        }
        serializer = ServiceAreaSerializer(data=data, context={'provider':self.provider.id})
        self.assertEqual(False, serializer.is_valid())
        
        data['area'] = [1,2,3]
        serializer = ServiceAreaSerializer(data=data, context={'provider':self.provider.id})
        self.assertEqual(False, serializer.is_valid())
        
        data['area'] = [[1,2], 2,3,4]
        serializer = ServiceAreaSerializer(data=data, context={'provider':self.provider.id})
        self.assertEqual(False, serializer.is_valid())
        
        data['area'] = [[1,2], [3,4], [5,6]]
        serializer = ServiceAreaSerializer(data=data, context={'provider':self.provider.id})
        self.assertEqual(False, serializer.is_valid())
        
        data['area'] = self.service_area_creation_data['area']
        serializer = ServiceAreaSerializer(data=data, context={'provider':self.provider.id})
        self.assertEqual(True, serializer.is_valid())
        
    def test_service_area_creation(self):
        """Test Service Area 'create' endpoint."""
        data = {
                "name": "Area1=51",
                "price": 10.00,
                "area": [
                    [0.0, 0.0],
                    [0.0, 1.0],
                    [1.0, 1.0],
                    [1.0, 0.0]
                ]
        }
        response = self.client.post(
            reverse(
                'providers:service-areas-list',
                kwargs={'provider_id':self.provider.id}
            ),
            data
        )
        
        self.assertEqual(response.status_code, 201)
    
    def test_service_area_detail(self):
        """Test Service Area 'retrieve' endpoint."""
        response = self.client.get(
            reverse(
                'providers:service-areas-detail',
                kwargs={
                    'provider_id':self.provider.id,
                    'pk': self.service_area.id
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        
    def test_service_area_list(self):
        """Test Service Area 'list' endpoint."""
        response = self.client.get(
            reverse(
                'providers:service-areas-list',
                kwargs={
                    'provider_id':self.provider.id
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        
    def test_service_area_update(self):
        """Test Service Area 'update' endpoint."""
        request_data = {
            "name": "Chernobil",
            "price": 44.00,
            "area": [
                [44.0, 22.34],
                [55.08, 12.35],
                [15.0, 1.0],
                [37.0, 56.0]
            ]
        }
        response = self.client.put(
            reverse(
                'providers:service-areas-detail',
                kwargs={
                    'provider_id':self.provider.id,
                    'pk': self.service_area.id
                }
            ),
            request_data
        )
        
    def test_service_area_partial_update(self):
        """Test Service Area 'partial_update' endpoint."""
        # 1st try
        request_data = {'name':'Disney'}
        
        response = self.client.patch(
            reverse(
                'providers:service-areas-detail',
                kwargs={
                    'provider_id':self.provider.id,
                    'pk': self.service_area.id
                }
            ),
            request_data
        )
        self.assertEqual(response.status_code, 200)
        
        # 2nd try
        request_data = {'price': 22.00}
        
        response = self.client.patch(
            reverse(
                'providers:service-areas-detail',
                kwargs={
                    'provider_id':self.provider.id,
                    'pk': self.service_area.id
                }
            ),
            request_data
        )
        self.assertEqual(response.status_code, 200)
        
        # 3rd try
        request_data = {
            'area': [
                [20.0, 14.0],
                [78.10, 113.0],
                [41.10, 1.30],
                [1.40, 70.42]
            ]
        }
        response = self.client.patch(
            reverse(
                'providers:service-areas-detail',
                kwargs={
                    'provider_id':self.provider.id,
                    'pk': self.service_area.id
                }
            ),
            request_data
        )
        self.assertEqual(response.status_code, 200)
    
    
    def test_service_area_destroy(self):
        """Test Service Area Viewset 'destroy' endpoint."""
        response = self.client.delete(
            reverse(
                'providers:service-areas-detail',
                kwargs={
                    'provider_id':self.provider.id,
                    'pk': self.service_area.id
                }
            )
        )
        self.assertEqual(response.status_code, 204)
        
    
class ActiveServiceAreaAPITestCase(APITestCase):
    """Test Active Service Area's enpoint."""
    
    def setUp(self):
        
        self.url = reverse(
            'providers:active-service-areas',
            kwargs={
                'lt':0.5,
                'lg':0.5
            }
        )
        
        self.user_data = {
            'username': 'username',
            'password': '$010203*',
            'first_name': 'first_name',
            'last_name': 'last_name'
        }
        self.provider_creation_data = {
            "name": "aprovidername",
            "email":"provideremail@ff.io",
            "language":"en",
            "currency": "USD",
            "phone_number": "+584120195481"
        }
        self.service_area_creation_data = {
            "name": "Area151",
            "price": 10.00,
            "area": [
                [0.0, 0.0],
                [0.0, 1.0],
                [1.0, 1.0],
                [1.0, 0.0]
            ]
        }
        
        self.user = User.objects.create(**self.user_data)
        self.provider = Provider.objects.create(
            **self.provider_creation_data,
            user=self.user
        )
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.creation_url = reverse(
            'providers:service-areas-list',
            kwargs={'provider_id':self.provider.id}
        )
        response = self.client.post(self.creation_url, self.service_area_creation_data)
        self.service_area = ServiceArea.objects.all()[0]
        
    def test_service_area_endpoint(self):
        response = self.client.get(self.url)
        
        # Check operation status
        self.assertEqual(response.status_code, 200)
        
        # Check if the polygon we created, that contains the point we defined
        # was returned.
        self.assertEqual(len(response.json()), 1)