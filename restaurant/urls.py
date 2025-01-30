# urls.py
from django.urls import path
from .views import home, menu, menu_item, about, reservations  # Import reservations view

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('menu/', menu, name='menu'),
    path('reservations/', reservations, name='reservations'),  # Keep reservations URL
    path('book/', reservations, name='book'),  # Add the 'book' URL pointing to the same 'reservations' view
]
