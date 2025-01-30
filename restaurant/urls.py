from django.urls import path
from .views import home, menu, menu_item, about, reservations  # Import reservations view

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('menu/', menu, name='menu'),
    path('reservations/', reservations, name='reservations'),  # Add the reservations URL pattern
]