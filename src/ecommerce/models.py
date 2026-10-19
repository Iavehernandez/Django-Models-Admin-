from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .validators import validate_blocked_words
from base.models import BasePublishModel # <------------------ importamos el modelo abstracto de base/models

from django.conf import settings

# [(VALOR EN BASE DE DATOS, VALOR PARA EL USUARIO)]
#PUBLISH_STATE_CHOICES = [
 #   ("BR", "BORRADOR"),
 #   ("PU", "PUBLICADO"),
 #  ("PR", "PRIVADO"),
# ]

# Create your models here.

User = settings.AUTH_USER_MODEL

class ProductModel(BasePublishModel):
    
    # state = models.CharField(max_length=2, choices=ProductStateOptions.choices, default=ProductStateOptions.DRAFT) # SE AGREGA UN LISTADO DE OPCIONES
    title = models.TextField()
    price = models.FloatField()
    description = models.CharField(blank=True)
    seller = models.CharField(blank=True)
    color = models.CharField(blank=True)
    product_dimensions = models.CharField(blank=True)
    slug = models.SlugField(null = True, blank=True, db_index=True)

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return f"/product/{self.slug}"

    def save(self, *args, **kwargs):
        validate_blocked_words(self.title)
        super().save(*args, **kwargs)

def slugify_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None or instance.slug == "":
        new_slug = slugify(instance.title)
        MyModel = instance.__class__ 
        qs = MyModel.objects.filter(slug__startswith=new_slug).exclude(id=instance.id)
        if qs.count() == 0:
            instance.slug = new_slug
        else:
            instance.slug = f"{new_slug}-{qs.count()}"

pre_save.connect(slugify_pre_save, sender=ProductModel) # Para conectar la funcion con nuestro modelo

   # def is_published(self):
    #    return self.state == self.ProductStateOptions.PUBLISHED # Si la instancia self state es igual a publicado entonces devuelve True