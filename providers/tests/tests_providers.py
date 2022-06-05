# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Models
from django.contrib.auth.models import User
from providers.models.providers import Provider

# Django
from django.urls import reverse


class ProvidersAPITestCase(APITestCase):
    """Test Provider's Viewset CRUD."""
    
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
        
        self.user = User.objects.create(**self.user_data)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
    def test_providers_create(self):
        """Test Providers 'create' endpoint."""
        response = self.client.post(reverse('providers:providers-list'),self.provider_creation_data)
        self.assertEqual(response.status_code, 201)
    
    def test_providers_detail(self):
        """Test Providers 'detail' endpoint."""
        provider = Provider.objects.create(**self.provider_creation_data, user=self.user)
        response = self.client.get(reverse('providers:providers-detail',kwargs={'pk':provider.id}))
        
        self.assertEqual(response.status_code, 200)
    
    def test_providers_list(self):
        """Test Providers 'list' endpoint."""
        provider = Provider.objects.create(**self.provider_creation_data, user=self.user)
        response = self.client.get(reverse('providers:providers-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    
    def test_providers_update(self):
        """Test Providers 'update' endpoint."""
        provider = Provider.objects.create(**self.provider_creation_data, user=self.user)

        update_data = {
            "name": "aprovider__name",
            "email":"provider_email@ff.io",
            "language":"es",
            "currency": "EUR",
            "phone_number": "+584162883163"
        }
        
        # Check difference between old and new data
        self.assertNotEqual(self.provider_creation_data, update_data)
        
        response = self.client.put(
            reverse('providers:providers-detail',kwargs={'pk':provider.id}),
            update_data
        )

        # Check status of the update request
        self.assertEqual(response.status_code, 200)
        
    
    def test_providers_partial_update(self):
        """Test Providers 'partial_update' endpoint."""
        provider = Provider.objects.create(**self.provider_creation_data, user=self.user)
        partial_update_data = {"name": "aprovider__name"}
                
        response = self.client.patch(
            reverse('providers:providers-detail',kwargs={'pk':provider.id}),
            partial_update_data
        )

        # Check status of the update request
        self.assertEqual(response.status_code, 200)
    
    def test_providers_delete(self):
        """Test Providers 'destroy' endpoint."""
        
        provider = Provider.objects.create(**self.provider_creation_data, user=self.user)
        response = self.client.delete(
            reverse('providers:providers-detail',kwargs={'pk':provider.id})
        )
        
        self.assertEqual(response.status_code, 204)