from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from .models import MenuItem
from . import serializers
from . import models
from django.views.generic import ListView

class MenuView(ListView):
    model = MenuItem
    template_name = "restaurant/menu.html"
    context_object_name = "menu_items"

def home(request):
    menu_items = MenuItem.objects.all()  # Retrieve all menu items
    return render(request, "restaurant/home.html", {"menu_items": menu_items})

def menu(request):
    menu_data = MenuItem.objects.all()  # Query all menu items
    return render(request, 'restaurant/menu.html', {"menu": menu_data})

def menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'restaurant/menu_item.html', {'menu_item': menu_item})

# Custom permission for admin-only write operations
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]
            return request.user.is_authenticated
        return request.user.is_staff  # Only admins can create or modify

# MenuItem views
class MenuItemView(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

# Booking views
class BookingView(generics.ListCreateAPIView):
    serializer_class = serializers.BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            models.Booking.objects.all()
            if self.request.user.is_superuser
            else models.Booking.objects.filter(user=self.request.user)
        )


