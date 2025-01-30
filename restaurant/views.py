from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from . import serializers


# Views for general pages

def home(request):
    menu_items = MenuItem.objects.filter(available=True)  # Filter available items
    print(menu_items)  # Debug: Print the queryset to confirm it's not empty
    return render(request, "restaurant/home.html", {"menu_items": menu_items})

def about(request):
    return render(request, "restaurant/about.html")

def menu(request):
    menu_data = MenuItem.objects.all()
    return render(request, 'restaurant/menu.html', {"menu": menu_data})

def menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'restaurant/menu_item.html', {'menu_item': menu_item})


# Reservation-related views

def reservations(request):
    bookings = Booking.objects.all()  # Add filtering logic for user if needed
    return render(request, "restaurant/reservations.html", {"bookings": bookings})

def booking_confirmation(request):
    return render(request, 'restaurant/confirmation.html')


def book_table(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['reservation_date']
            reservation_slot = form.cleaned_data['reservation_slot']
            guests = form.cleaned_data['guests']

            try:
                # Try to assign a table based on the reservation slot and number of guests
                table = get_available_table(reservation_slot, guests)
                form.instance.table = table
            except ValidationError as e:
                form.add_error('guests', str(e))
                return render(request, 'restaurant/book.html', {'form': form})

            # Check if the slot is already booked
            if Booking.objects.filter(reservation_date=reservation_date, reservation_slot=reservation_slot).exists():
                form.add_error('reservation_slot', 'This time slot is already booked.')
            else:
                form.save()
                return redirect('booking_confirmation')

    else:
        form = BookingForm()

    return render(request, 'restaurant/book.html', {'form': form})

# Helper function for checking table availability

def get_available_table(reservation_slot, guests):
    available_tables = Table.objects.filter(seats__gte=guests)

    if not available_tables:
        raise ValidationError("No available tables for the requested number of guests.")

    for table in available_tables:
        if not Booking.objects.filter(table=table, reservation_slot=reservation_slot).exists():
            return table

    raise ValidationError("No available tables for the requested time slot.")


# API-related views

# views.py

def check_availability(request):
    """
    Checks if the requested time slot is available for a given date.
    Example request: GET /api/check-availability/?date=2025-01-30&time=12:00
    """
    date = request.GET.get('date')
    time = request.GET.get('time')
    
    if not date or not time:
        return JsonResponse({"error": "Date and time parameters are required."}, status=400)

    # Check if the time slot is already booked for the selected date
    bookings = Booking.objects.filter(reservation_date=date, reservation_time=time)
    if bookings.exists():
        return JsonResponse({"available": False})
    return JsonResponse({"available": True})

def get_booked_slots(request):
    """
    Returns a list of all booked slots for a specific date.
    Example request: GET /api/booked-slots/?date=2025-01-30
    """
    date = request.GET.get('date')
    if not date:
        return JsonResponse({"error": "Date parameter is required."}, status=400)

    bookings = Booking.objects.filter(reservation_date=date)
    booked_slots = bookings.values_list('reservation_time', flat=True)

    return JsonResponse({"booked_slots": list(booked_slots)}, safe=False)

# API views using Django REST Framework

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingView(generics.ListCreateAPIView):
    serializer_class = serializers.BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        reservation_date = serializer.validated_data['reservation_date']
        reservation_slot = serializer.validated_data['reservation_slot']

        if Booking.objects.filter(reservation_date=reservation_date, reservation_slot=reservation_slot).exists():
            raise ValidationError("This slot is already booked.")

        serializer.save(user=self.request.user)


# Custom permissions for admin-only operations

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission class for read-only access to non-admin users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]
            return request.user.is_authenticated
        return request.user.is_staff  # Only admins can create or modify
