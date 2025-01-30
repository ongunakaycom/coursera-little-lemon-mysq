from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator  # Add this import

class Table(models.Model):
    """Represents a restaurant table with its capacity."""
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)"

class Booking(models.Model):
    """Represents a restaurant booking/reservation."""
    TIME_SLOTS = [
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('13:00', '1:00 PM'),
        ('13:30', '1:30 PM'),
        ('14:00', '2:00 PM'),
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

class BookingForm(forms.ModelForm):
    TIME_SLOTS = [
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('13:00', '1:00 PM'),
        ('13:30', '1:30 PM'),
        ('14:00', '2:00 PM'),
    ]

    reservation_time = forms.ChoiceField(
        choices=TIME_SLOTS, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )  # Adding form-control for styling

    class Meta:
        model = Booking
        fields = ['first_name', 'reservation_date', 'reservation_time', 'guests', 'table']  # Ensure the fields are correct

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields['first_name'].initial = self.user.get_full_name()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and self.user.is_authenticated:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

class MenuItem(models.Model):
    """Represents a menu item in the restaurant."""
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