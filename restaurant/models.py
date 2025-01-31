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
    """Represents a restaurant booking/reservation."""
    TIME_SLOTS = [
        ('10:00', '10:00 AM'),
        ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'),
        ('11:30', '11:30 AM'),
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('13:00', '1:00 PM'),
        ('13:30', '1:30 PM'),
        ('14:00', '2:00 PM'),
        ('14:30', '2:30 PM'),
        ('15:00', '3:00 PM'),
        ('18:30', '6:30 PM'),
        ('21:30', '9:30 PM'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    first_name = models.CharField(max_length=100, default="Guest", verbose_name="Guest Name")
    reservation_date = models.DateField()
    reservation_time = models.CharField(max_length=5, choices=TIME_SLOTS, verbose_name="Time Slot")
    guests = models.PositiveIntegerField(default=1, verbose_name="Number of Guests")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings', verbose_name="Table Number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-reservation_date', '-reservation_time']
        unique_together = ['reservation_date', 'reservation_time', 'table']

    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} {self.reservation_time}"


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
