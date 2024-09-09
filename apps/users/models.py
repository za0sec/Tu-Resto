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
    branch = models.ForeignKey('restaurant.Branch', on_delete=models.CASCADE, related_name='branch_employees', null=True, blank=True)

    objects = InheritanceManager()


'''
Modela a un empleado de una branch especifica. Por eso guarda branch
'''
class BranchStaff(Employee):
    # branch = models.ForeignKey('restaurant.Branch', on_delete=models.CASCADE, related_name='branch_employees', null=True, blank=True)
    pass


class Waiter(Employee):
    pass


class Cashier(Employee):
    pass


class Kitchen(Employee):
    pass


# TODO: RENAME TO MANAGER
'''
Modela al administrador de un restaurant -- todas sus branches
'''
class Manager(Employee):
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE, related_name='restaurant_managers', null=True, blank=True)
    pass


class Admin(Person):
    pass
