# LittleLemonAPI/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, ItemOfTheDay
from .serializers import BookingSerializer, ItemOfTheDaySerializer

# View for listing all bookings
class BookingListAPIView(APIView):
    def get(self, request):
        bookings = Booking.objects.all()  # Fetch all bookings
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

# View for updating the item of the day (only accessible by managers)
class UpdateItemOfTheDay(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        if request.user.groups.filter(name="Manager").exists():
            menu_item = request.data['menu_item']
            item_of_the_day, created = ItemOfTheDay.objects.update_or_create(menu_item=menu_item)
            return Response(ItemOfTheDaySerializer(item_of_the_day).data)
        return Response({"detail": "You do not have permission to perform this action."}, status=403)
