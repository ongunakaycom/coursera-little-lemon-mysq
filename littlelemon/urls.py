from django.contrib import admin
from django.urls import path, include
from restaurant import views as restaurant_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("restaurant/", include("restaurant.urls")),
    path("auth/", include("authn.urls")),
    path("", restaurant_views.home, name="home"),  # Root URL to restaurant home view
]
