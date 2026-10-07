from django.db import models
from .validators import validate_blocked_words

# [(VALOR EN BASE DE DATOS, VALOR PARA EL USUARIO)]
PUBLISH_STATE_CHOICES = [
    ("BR", "BORRADOR"),
    ("PU", "PUBLICADO"),
    ("PR", "PRIVADO"),
]

# Create your models here.

class ProductModel(models.Model):
    state = models.CharField(max_length=2, choices=PUBLISH_STATE_CHOICES, default="BR") # SE AGREGA UN LISTADO DE OPCIONES
    title = models.TextField()
    price = models.FloatField()
    description = models.CharField(blank=True)
    seller = models.CharField(blank=True)
    color = models.CharField(blank=True)
    product_dimensions = models.CharField(blank=True)

    def save(self, *args, **kwargs):
        validate_blocked_words(self.title)
        super().save(*args, **kwargs)

    def is_published(self):
        return self.state == "PU" # Si en la instancia el state esta en PU devuelve verdadero, sino devuelve Falso