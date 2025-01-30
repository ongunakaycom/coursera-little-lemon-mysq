# LittleLemonAPI/urls.py
from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework_simplejwt.views import TokenRefreshView

# Import your custom views (e.g., UpdateItemOfTheDayView, AssignDeliveryCrewView, and BookingListAPIView)
from .views import UpdateItemOfTheDay, BookingListAPIView, AssignDeliveryCrewView

urlpatterns = [
    # Other urls...

    # JWT authentication endpoints
    path('auth/login/', TokenCreateView.as_view(), name='login'),
    path('auth/logout/', TokenDestroyView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # To handle refreshing of the token

    # Custom manager actions
    path('item-of-the-day/update/', UpdateItemOfTheDay.as_view(), name='update-item-of-the-day'),
    path('bookings/', BookingListAPIView.as_view(), name='bookings-list'),  # Add this line for bookings
    path('delivery-crew/assign/', AssignDeliveryCrewView.as_view(), name='assign-delivery-crew'),
]
