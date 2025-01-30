# LittleLemonAPI/models.py
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        permissions = [
            ("add_category", "Can add category"),
            ("change_category", "Can change category"),
            ("delete_category", "Can delete category"),
            ("view_category", "Can view category"),
        ]

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')

    def __str__(self):
        return self.name

class DeliveryCrew(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - Delivery Crew"

class ItemOfTheDay(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Item of the day: {self.menu_item.name}"

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(DeliveryCrew, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.id} for {self.customer.username}"
