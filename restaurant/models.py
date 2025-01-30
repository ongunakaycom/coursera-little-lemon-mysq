from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="Guest")  # Add default
    reservation_date = models.DateField(default=timezone.now)
    reservation_slot = models.TimeField()
    guests = models.IntegerField()
    table = models.IntegerField()

    class Meta:
        unique_together = ('reservation_date', 'reservation_slot')

    def __str__(self):
        return f"{self.first_name} - Table {self.table} on {self.reservation_date} at {self.reservation_slot}"

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000, default='')
    category = models.CharField(max_length=50, choices=[('Starter', 'Starter'), ('Main', 'Main'), ('Dessert', 'Dessert')], default='Starter')

    def __str__(self):
        return self.name

