from django.db import models

# Create your models here.

class Reservation(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    message = models.TextField()
    branch = models.ForeignKey('restaurant.Branch', on_delete=models.CASCADE)
    table = models.ForeignKey('restaurant.Table', on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
             models.UniqueConstraint(fields=['date', 'time', 'table'], name='unique_reservation')
            ]
    
    def __str__(self):
        return self.name        