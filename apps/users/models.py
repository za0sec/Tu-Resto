from django.db import models

# aca van a ir todos los relacionados con PERSONAS


class User(models.Model):
    """ Physical person """
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Employee(User):
    """ Restaurant person """
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)


class Waiter(Employee):
    pass


class Cashier(Employee):
    pass


class Kitchen(Employee):
    pass


class Manager(Employee):
    pass


class Admin(User):
    pass
