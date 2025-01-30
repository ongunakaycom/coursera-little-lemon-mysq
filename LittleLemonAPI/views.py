# LittleLemonAPI/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ItemOfTheDay, MenuItem
from .serializers import ItemOfTheDaySerializer

class UpdateItemOfTheDay(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Check if the user is a manager
        if request.user.groups.filter(name="Manager").exists():
            menu_item_id = request.data.get('menu_item')  # Assuming you're passing the ID
            if not menu_item_id:
                return Response({"detail": "Menu item ID is required."}, status=400)

            # Check if the menu item exists
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
            except MenuItem.DoesNotExist:
                return Response({"detail": "Menu item not found."}, status=404)

            # Update or create the ItemOfTheDay object
            item_of_the_day, created = ItemOfTheDay.objects.update_or_create(
                menu_item=menu_item,
                defaults={'menu_item': menu_item}  # Adjust if there are other fields to update
            )

            # Return the updated ItemOfTheDay object
            return Response(ItemOfTheDaySerializer(item_of_the_day).data)
        
        # If the user is not a manager, return a permission error
        return Response({"detail": "You do not have permission to perform this action."}, status=403)
