from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guests = models.IntegerField()
    table = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        app_label = 'restaurant'  # Explicitly declare app_label

    def __str__(self):
        return f"{self.user.first_name}, {self.table}: {self.date}"

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000, default='')
    category = models.CharField(max_length=50, choices=[('Starter', 'Starter'), ('Main', 'Main'), ('Dessert', 'Dessert')], default='Starter')

    def __str__(self):
        return self.name

