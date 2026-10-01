from django.db import models

# Create your models here.

class ProductModel(models.Model):
    title = models.TextField()
    price = models.FloatField()
    description = models.CharField(blank=True)
    seller = models.CharField(blank=True)
    color = models.CharField(blank=True)
    product_dimensions = models.CharField(blank=True)
