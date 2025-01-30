from django.contrib import admin
from .models import Booking, MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'available', 'created_at', 'updated_at')  # Display relevant fields
    list_filter = ('category', 'available')  # Filter by category and availability
    search_fields = ('name', 'category')  # Search by name and category
    ordering = ('category',)  # Order by category

admin.site.register(Booking)
admin.site.register(MenuItem, MenuItemAdmin)
