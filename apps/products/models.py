from django.db import models

# Create your models here.


class Item(models.Model):
    """ Restaurant Products """
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='products', null=True, blank=True)
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name