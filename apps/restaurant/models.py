from django.db import models

# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.URLField()

    def __str__(self):
        return self.name


class Branch(models.Model):
    """ Restaurant branch """
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    employees = models.ForeignKey('users.Employee', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Table(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    waiter = models.ForeignKey('users.Waiter', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Table {self.number} at {self.branch.name}"
