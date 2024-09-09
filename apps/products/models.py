from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='categories', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Restaurant Products """
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='products', null=True, blank=True)
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null = True)
    
    def __str__(self):
        return self.name


class CategoryExtra(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='categories', null=True, blank=True)

    def __str__(self):
        return self.name


class ProductExtra(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='products', null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    product = models.ForeignKey(Product, related_name='product_extras', on_delete=models.CASCADE)
    category = models.ForeignKey('CategoryExtra', on_delete=models.SET_NULL, null = True, blank=True)

    def __str__(self):
        return self.name
    