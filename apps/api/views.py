# Create your views here.
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.conf import settings

from .permissions import IsWaiter, IsManager, IsAdmin, AllowAny
from .serializers import RestaurantSerializer, BranchSerializer, ProductSerializer, ManagerSerializer, WaiterSerializer, \
    KitchenSerializer, PlanSerializer, EmployeeSerializer, TakeAwayOrderSerializer

from apps.restaurant.models import Restaurant,Branch
from apps.products.models import Item
from ..users.models import Person, Manager, Waiter, Kitchen, Employee
from apps.subscription.models import Plan

from apps.orders.models import TakeAwayOrder
from apps.wpp.views import notifyOrderReady

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

class RestaurantManager(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        manager = restaurant.restaurant_managers.first()
        serializer = ManagerSerializer(manager)
        return Response(serializer.data)


# RUD Retrieve - Update - Destroy
class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        manager = instance.restaurant_managers.first()
        if manager:
            manager_serializer = ManagerSerializer(manager)
            data['manager'] = manager_serializer.data
        else:
            data['manager'] = None

        return Response(data)


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
    permission_classes = [IsWaiter | IsManager | IsAdmin]
    serializer_class = ProductSerializer
    queryset = Item.objects.all()


class ProductCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = ProductSerializer
    queryset = Item.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | IsManager | IsWaiter]
    queryset = Item.objects.all()
    serializer_class = ProductSerializer


class ManagerCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class ManagerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class WaiterCreate(generics.CreateAPIView):
    permission_classes = [IsManager | IsAdmin]
    queryset = Waiter.objects.all()
    serializer_class = WaiterSerializer


class KitchenCreate(generics.CreateAPIView):
    permission_classes = [IsManager | IsAdmin]
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


class Employees(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            # Validar el token
            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

# ORDERS
class TakeAwayOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = TakeAwayOrder.objects.all()
    serializer_class = TakeAwayOrderSerializer
    
    def perform_update(self, serializer):
        # Llama a la implementación por defecto para realizar la actualización
        serializer.save()
        self.handle_ready_status(self.get_object())

    def handle_ready_status(self, new_order):
        if new_order.ready is True:
            notifyOrderReady(new_order.phone_number, new_order)
