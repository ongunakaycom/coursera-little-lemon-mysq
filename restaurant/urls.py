from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('menu/<int:pk>/', views.menu_item, name='menu_item'),
    path('reservations/', views.reservations, name='reservations'),
    path('book/', views.book_table, name='book'),
    path('confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('api/booked-slots/', views.get_booked_slots, name='get_booked_slots'),
]
