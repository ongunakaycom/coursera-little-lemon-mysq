# LittleLemonAPI/serializers.py
from rest_framework import serializers
from .models import ItemOfTheDay

class ItemOfTheDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOfTheDay
        fields = ['menu_item']  # Include any additional fields if necessary

# LittleLemonAPI/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ItemOfTheDay
from .serializers import ItemOfTheDaySerializer

class UpdateItemOfTheDay(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        if request.user.groups.filter(name="Manager").exists():
            menu_item = request.data['menu_item']
            item_of_the_day, created = ItemOfTheDay.objects.update_or_create(menu_item=menu_item)
            return Response(ItemOfTheDaySerializer(item_of_the_day).data)
        return Response({"detail": "You do not have permission to perform this action."}, status=403)
