from rest_framework import serializers
from . import models

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = "__all__"

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = "__all__"