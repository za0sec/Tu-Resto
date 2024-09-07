# Create your views here.
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .permissions import IsWaiter, IsManager, IsAdmin, AllowAny
from .serializers import RestaurantSerializer, BranchSerializer, ProductSerializer, ManagerSerializer, WaiterSerializer, \
    KitchenSerializer, PlanSerializer, EmployeeSerializer

from apps.restaurant.models import Restaurant,Branch
from apps.products.models import Item
from ..users.models import Person, Manager, Waiter, Kitchen, Employee
from apps.subscription.models import Plan


# Subscription
class Plans(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


# Restaurant
# ListAPIView already generates the response. No need to define a get method.
class Restaurants(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()


# C Create
class RestaurantCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# RUD Retrieve - Update - Destroy
class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# Branches
class BranchCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin, IsManager]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


# RUD Retrieve - Update - Destroy
class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin, IsManager]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class Branches(generics.ListAPIView):
    permission_classes = [IsAdmin, IsManager]
    serializer_class = BranchSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Branch.objects.filter(restaurant_id=restaurant_id)


# PRODUCTS
class Products(generics.ListAPIView):
    permission_classes = [IsWaiter, IsManager, IsAdmin]
    serializer_class = ProductSerializer
    queryset = Item.objects.all()


class ProductCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin, IsManager]
    serializer_class = ProductSerializer
    queryset = Item.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin, IsManager, IsWaiter]
    queryset = Item.objects.all()
    serializer_class = ProductSerializer


class ManagerCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class WaiterCreate(generics.CreateAPIView):
    permission_classes = [IsManager, IsAdmin]
    queryset = Waiter.objects.all()
    serializer_class = WaiterSerializer


class KitchenCreate(generics.CreateAPIView):
    permission_classes = [IsManager, IsAdmin]
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


class Employees(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()