# F:\HDD\GitHub\coursera-little-lemon-mysql\restaurant\forms.py

from django.db import models
from django import forms
from datetime import time, datetime, timedelta
from django.contrib.auth.models import User
from restaurant.models import Table
from .models import Booking
from django.shortcuts import render, redirect
from django.contrib import messages


def book_table(request):
    if request.method == "POST":
        # Import BookingForm here to avoid circular import
        from .forms import BookingForm
        
        form = BookingForm(request.POST)  # Bind form to POST data
        if form.is_valid():  # Validate the form
            # Save the form data to the database
            form.save()
            # Show a success message to the user
            messages.success(request, "Your booking was successful!")
            return redirect('book')  # Redirect to the same page or another page
        else:
            # Handle form errors
            messages.error(request, "There was an issue with your booking.")
    else:
        # Import BookingForm here as well
        from .forms import BookingForm
        form = BookingForm()  # If not POST, create an empty form

    return render(request, 'restaurant/book.html', {'form': form})

def add_table(request):
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()  # Save new table data to the database
            messages.success(request, "New table added successfully!")
            return redirect('tables')  # Redirect to a page showing the tables
        else:
            messages.error(request, "There was an issue adding the table.")
    else:
        form = TableForm()

    return render(request, 'restaurant/add_table.html', {'form': form})

# TableForm moved to be defined here, no change needed
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