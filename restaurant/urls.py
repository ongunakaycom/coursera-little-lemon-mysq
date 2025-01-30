from django.urls import path
from .views import home, menu, menu_item

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('menu/', menu, name='menu'),  # Menu page
    path('menu_item/<int:pk>/', menu_item, name='menu_item'),  # Individual menu item
    # other paths
]
