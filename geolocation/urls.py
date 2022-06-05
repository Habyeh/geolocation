"""
geolocation URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Providers
    path('', include(('providers.urls.module_urls', 'providers'), namespace='providers')),
]