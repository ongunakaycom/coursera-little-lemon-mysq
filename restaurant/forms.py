# restaurant/forms.py
from django import forms
from .models import Booking, Table

class BookingForm(forms.ModelForm):
    TIME_SLOTS = [
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('13:00', '1:00 PM'),
        ('13:30', '1:30 PM'),
        ('14:00', '2:00 PM'),
        # Add more slots as needed
    ]

    reservation_time = forms.ChoiceField(choices=TIME_SLOTS)  # Updated field name

    class Meta:
        model = Booking
        fields = ['first_name', 'reservation_date', 'reservation_time', 'guests', 'table']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields['first_name'].initial = self.user.get_full_name()

    def save(self, commit=True):
        instance = super().save(commit=False)  # Get the form instance without saving yet
        if self.user and self.user.is_authenticated:  # Check if the user is authenticated
            instance.user = self.user  # Assign the user to the booking
        if commit:
            instance.save()  # Save the instance to the database
        return instance
