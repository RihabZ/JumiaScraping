from django.db import models

class Smartphone(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    brand = models.CharField(max_length=50)
    link = models.URLField()

    def __str__(self):
        return self.name
