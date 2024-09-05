from django.urls import path
from .views import *
from .authenticator import *


urlpatterns = [
    path("restaurant/create", RestaurantCreate.as_view(), name="restaurant_create"),
]