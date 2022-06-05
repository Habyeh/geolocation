# Django
from django.db import models

# Utilities
from utils.models import BaseModel


class ServiceArea(BaseModel):
    """Service Area model.
    
    A Service Area is an entity, that stores information
    about the area in which a provider works.
    """
    
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.JSONField()
    
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        """Return Service Area name."""
        
        return f"Area name: {self.name} | Provider: {self.provider.name}"