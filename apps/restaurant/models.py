from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.URLField()
    banner = models.ImageField(upload_to='media/restaurants/banners/', null=True, blank=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    """ Restaurant branch """
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='branches')
    employees = models.ForeignKey('users.Employee', null=True, on_delete=models.SET_NULL, related_name='branch_all_employees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'address'], name='unique_branch')
        ]

    def __str__(self):
        return f"{self.name} at {self.address}"


class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    bookable = models.BooleanField(default=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    waiter = models.ForeignKey('users.Waiter', on_delete=models.SET_NULL, null=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['position_x', 'position_y', 'branch', 'number'], name='unique_table')
    #     ]

    def __str__(self):
        return f"Table {self.number} at {self.branch.name}"

