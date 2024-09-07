from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *
from .authenticator import *

urlpatterns = [

    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Subscription
    path("plans/", Plans.as_view(), name="plans"),

    # Auth
    path("auth/login", PersonTokenObtainPairView.as_view(), name="api_login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="api_refresh_token"),

    # Restaurants
    path("restaurants", Restaurants.as_view(), name="restaurant_list"),
    path('restaurant/<int:pk>', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path("restaurant/create", RestaurantCreate.as_view(), name="restaurant_create"),
    path('restaurant/<int:restaurant_id>/branches', Branches.as_view(), name='restaurant-branches'),

    # Branches
    path("branch/create", BranchCreate.as_view(), name="branch_create"),
    path("branch/<int:pk>", BranchDetailView.as_view(), name="branch-detail-view"),

    # Products
    path("products/", Products.as_view(), name="product_list"),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path("product/create", ProductCreate.as_view(), name="product_create"),

    # Total Employees
    path("employees", Employees.as_view(), name="employees_list"),

    # Manager
    path("users/manager/create", ManagerCreate.as_view(), name="manager_create"),
    path("users/waiter/create", WaiterCreate.as_view(), name="waiter_create"),
]
