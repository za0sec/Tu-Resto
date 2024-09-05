from django.contrib.auth.models import User
from django.db import models

# aca van a ir todos los relacionados con PERSONAS


class Person(models.Model):
    """ Physical person """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Employee(Person):
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


class Admin(Person):
    pass
