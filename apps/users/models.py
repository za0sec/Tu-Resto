from django.contrib.auth.models import User
from django.db import models
from model_utils.managers import InheritanceManager


class Person(models.Model):
    """ Physical person """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = InheritanceManager()

    def __str__(self):
        return self.user.username


class Employee(Person):
    """ Restaurant person """
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='employees')

    objects = InheritanceManager()


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
