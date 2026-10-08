from django.db import models
from .validators import validate_blocked_words
from base.models import BasePublishModel # <------------------ importamos el modelo abstracto de base/models

# [(VALOR EN BASE DE DATOS, VALOR PARA EL USUARIO)]
#PUBLISH_STATE_CHOICES = [
 #   ("BR", "BORRADOR"),
 #   ("PU", "PUBLICADO"),
 #  ("PR", "PRIVADO"),
# ]

# Create your models here.

class ProductModel(BasePublishModel):
    
    # state = models.CharField(max_length=2, choices=ProductStateOptions.choices, default=ProductStateOptions.DRAFT) # SE AGREGA UN LISTADO DE OPCIONES
    title = models.TextField()
    price = models.FloatField()
    description = models.CharField(blank=True)
    seller = models.CharField(blank=True)
    color = models.CharField(blank=True)
    product_dimensions = models.CharField(blank=True)

    def save(self, *args, **kwargs):
        validate_blocked_words(self.title)
        super().save(*args, **kwargs)

   # def is_published(self):
    #    return self.state == self.ProductStateOptions.PUBLISHED # Si la instancia self state es igual a publicado entonces devuelve True