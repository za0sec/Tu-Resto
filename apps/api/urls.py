from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views

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
    path("restaurant/<int:pk>/manager", RestaurantManager.as_view(), name="restaurant-manager"),
    path('restaurant/<int:restaurant_id>/branches', Branches.as_view(), name='restaurant-branches'),

    # Branches
    path("branch/create", BranchCreate.as_view(), name="branch_create"),
    path("branch/<int:pk>", BranchDetailView.as_view(), name="branch-detail-view"),

    # Total Employees
    path("employees", Employees.as_view(), name="employees_list"),

    # Staff
    path("user/profile", UserProfile.as_view(), name="user_profile"),

    # Manager
    path("users/manager/create", ManagerCreate.as_view(), name="manager_create"),
    path("users/manager/<int:pk>", ManagerDetailView.as_view(), name="manager_detail"),
    path("users/waiter/create", WaiterCreate.as_view(), name="waiter_create"),
    path('reset-password/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    
    # Orders
    path("orders", Orders.as_view(), name="orders"),
    path("orders/daily/<str:date>", DailyOrders.as_view(), name="daily_orders"),
    path("order/create", OrderCreate.as_view(), name="order_create"),
    path("order/<int:pk>", OrderDetailView.as_view(), name="order-detail"),
    
    # takeawayorders
    path("order/takeaway/create", TakeAwayOrderCreate.as_view(), name="takeaway_order_create"),
    path("order/takeaway/<int:pk>", TakeAwayOrderDetailView.as_view(), name="takeaway_order_detail"),

    # deliveryorders
    path("order/delivery/create", DeliveryOrderCreate.as_view(), name="delivery_order_create"),
    path("order/delivery/<int:pk>", DeliveryOrderDetailView.as_view(), name="delivery_order_detail"),

    # tableorders
    path("order/table/create", TableOrderCreate.as_view(), name="table_order_create"),
    path("order/table/<int:pk>", TableOrderDetailView.as_view(), name="table_order_detail"),
    
    # OrderItem
    path("orderitem/create", OrderItemCreate.as_view(), name="orderitem_create"),
    path("orderitem/<int:pk>", OrderItemDetailView.as_view(), name="orderitem_detail"),
    path("orderitems", OrderItems.as_view(), name="orderitem_list"),
    
    # Categorías
    path("categories/", Categories.as_view(), name="category_list"),
    path("category/create", CategoryCreate.as_view(), name="category_create"),
    path("category/<int:pk>", CategoryDetailView.as_view(), name="category_detail"),

    # Products
    path("products/", Products.as_view(), name="product_list"),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path("product/create", ProductCreate.as_view(), name="product_create"),

    # Categorías Extra
    path("categories-extra/", CategoriesExtra.as_view(), name="category_extra_list"),
    path("category-extra/create", CategoryExtraCreate.as_view(), name="category_extra_create"),
    path("category-extra/<int:pk>", CategoryExtraDetailView.as_view(), name="category_extra_detail"),

    # Planes de suscripción
    path("plans/", Plans.as_view(), name="plan_list"),
]
