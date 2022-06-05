# Django
from django.urls import path, include

# Views
from providers.api_views.auth_api import UserViewSet
from providers.api_views.providers_api import (
    ProviderViewSet,
    ActiveProvidersAPIView
)
from providers.api_views.service_areas_api import ServiceAreaViewSet

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Providers
router.register(r'providers', ProviderViewSet, basename='providers')

# Service Area
router.register(
    r'providers/(?P<provider_id>[0-9]+)/service-areas',
    ServiceAreaViewSet,
    basename='service-areas'
)

# Users
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('active-providers/<lt>/<lg>/', ActiveProvidersAPIView.as_view(), name='active-service-areas')
]