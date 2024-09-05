from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *
from .authenticator import *


urlpatterns = [
    # Vistas opcionales para Swagger y Redoc UI
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Auth
    path("auth/login", PersonTokenObtainPairView.as_view(), name="api_login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="api_refresh_token"),

    # Restaurants
    path("restaurants/", Restaurants.as_view(), name="restaurant_list"),
    path('restaurant/<int:pk>', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path("restaurant/create", RestaurantCreate.as_view(), name="restaurant_create"),
    path('restaurant/<int:restaurant_id>/branches', Branches.as_view(), name='restaurant-branches'),


    # Branches
    path("branch/create", BranchCreate.as_view(), name="branch_create"),
    path("branch/<int:pk>", BranchDetailView.as_view(), name="branch-detail-view"),


    # Users
    # path("users/", MyInformation.as_view(), name="api_my_information"),
]