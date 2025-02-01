# restaurant/urls.py
from django.urls import path
from . import views

app_name = 'restaurant'  # Namespace for the app

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),  # Correctly defined
    path('menu/', views.menu, name='menu'),
    path('menu/<int:pk>/', views.menu_item, name='menu_item'),
    path('reservations/', views.reservations, name='reservations'),  # Define the 'reservations' URL
    path('book/', views.book_table, name='book'),
    path('confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('api/booked-slots/', views.get_booked_slots, name='get_booked_slots'),
    path('api/check-availability/', views.check_availability, name='check_availability'),
]