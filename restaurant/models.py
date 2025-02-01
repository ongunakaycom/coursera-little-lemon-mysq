# HDD\GitHub\coursera-little-lemon-mysql\restaurant\models.py

from django.db import models
from django.contrib.auth.models import User
from datetime import time, datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


# Table model
class Table(models.Model):
    number = models.IntegerField()
    seats = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)"

# MenuItem model
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('ST', 'Starter'),
        ('MN', 'Main Course'),
        ('DS', 'Dessert'),
        ('BE', 'Beverage'),
    ]
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(max_length=1000, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='MN')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"


# Booking model
class Booking(models.Model):
    first_name = models.CharField(max_length=100)
    reservation_date = models.DateField()
    reservation_time = models.CharField(max_length=5)  # Store as a string (e.g., "10:00")
    
    # Optional field for table, can be left blank if you don't want to assign a table
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Booking for {self.first_name} on {self.reservation_date} at {self.reservation_time}"


# Helper function to generate dynamic time slots
def generate_time_slots(start_time, end_time, interval=30):
    """Generate available time slots within restaurant hours."""
    slots = []
    current_time = start_time
    while current_time < end_time:
        formatted_time = current_time.strftime("%H:%M")  # e.g., "10:00"
        display_time = current_time.strftime("%I:%M %p")  # e.g., "10:00 AM"
        slots.append((formatted_time, display_time))
        current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=interval)).time()
    return slots


# Reservation model
class Reservation(models.Model):
    reservation_time = models.TimeField()
    reservation_date = models.DateField()
    guests = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Reservation for {self.reservation_date} at {self.reservation_time}"
