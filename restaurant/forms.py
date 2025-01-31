# F:\HDD\GitHub\coursera-little-lemon-mysql\restaurant\forms.py

from django.db import models
from django import forms
from datetime import time, datetime, timedelta
from django.contrib.auth.models import User
from restaurant.models import Table
from .models import Booking


# TableForm
class TableForm(forms.Form):
    """Represents a restaurant table with its capacity."""
    number = forms.IntegerField()  # Form field instead of model field
    seats = forms.IntegerField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)"


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


# BookingForm with default time slots
class BookingForm(forms.ModelForm):
    DEFAULT_TIME_SLOTS = generate_time_slots(time(10, 0), time(22, 0), interval=30)

    reservation_time = forms.ChoiceField(
        choices=DEFAULT_TIME_SLOTS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['first_name', 'reservation_date', 'reservation_time', 'guests', 'table']

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


# In forms.py
class TableFormModel(models.Model):
    """Represents a restaurant table with its capacity."""
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Table {self.number} ({self.seats} seats)"
