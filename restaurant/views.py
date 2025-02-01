from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import MenuItem, Table, Booking
from django.contrib import messages
from django.utils.dateparse import parse_date
from restaurant.serializers import MenuItemSerializer, BookingSerializer  # Import both serializers

# Views for general pages
def home(request):
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, "restaurant/home.html", {"menu_items": menu_items})

def about(request):
    return render(request, "restaurant/about.html")

def menu(request):
    menu_data = MenuItem.objects.all()
    return render(request, 'restaurant/menu.html', {"menu": menu_data})

def menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'restaurant/menu_item.html', {'menu_item': menu_item})

# Reservation Views
def reservations(request):
    bookings = Booking.objects.all()
    return render(request, "restaurant/reservations.html", {"bookings": bookings})

def booking_confirmation(request):
    return render(request, 'restaurant/confirmation.html')

def book_table(request):
    if request.method == 'POST':
        # Import BookingForm locally inside the function
        from .forms import BookingForm
        
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save()
            print(f"Booking saved: {booking}")  # Debugging output
            messages.success(request, 'Your table has been booked successfully!')
            return redirect('restaurant:booking_confirmation')
        else:
            print("Form errors:", form.errors)  # Debugging output
            messages.error(request, 'There were some errors in your form submission.')
    else:
        # Import BookingForm here as well
        from .forms import BookingForm
        form = BookingForm(user=request.user)

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
def check_availability(request):
    """Check if a time slot is available for a given date."""
    date = request.GET.get('date')
    time = request.GET.get('time')
    
    if not date or not time:
        return JsonResponse({"error": "Date and time parameters are required."}, status=400)

    if Booking.objects.filter(reservation_date=date, reservation_time=time).exists():
        return JsonResponse({"available": False})
    return JsonResponse({"available": True})

def get_booked_slots(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({"error": "No date provided"}, status=400)

    try:
        parsed_date = parse_date(date)
        if not parsed_date:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        booked_slots = Booking.objects.filter(reservation_date=parsed_date).values_list('reservation_time', flat=True)
        return JsonResponse({"booked_slots": list(booked_slots)})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# DRF Views
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer  # Use the imported MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer  # Use the imported MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer  # Use the imported BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        reservation_date = serializer.validated_data['reservation_date']
        reservation_time = serializer.validated_data['reservation_time']

        if Booking.objects.filter(reservation_date=reservation_date, reservation_time=reservation_time).exists():
            raise ValidationError("This slot is already booked.")
        serializer.save(user=self.request.user)
