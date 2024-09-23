# Create your views here.
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.conf import settings

from .permissions import IsManager, IsAdmin, AllowAny, IsBranchStaff
from .serializers import *

from apps.restaurant.models import Restaurant,Branch
from apps.products.models import Product, Category, CategoryExtra
from ..users.models import Person, Manager, Waiter, Kitchen, Employee, BranchStaff
from apps.subscription.models import Plan

from apps.orders.models import TakeAwayOrder, Order, TableOrder, DeliveryOrder, OrderItem
from apps.wpp.views import notifyOrderReady

class HelloWorld(APIView):
    permission_classes = [AllowAny]
    def get(request):
        return "Hello"


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


# User Profile
class UserProfile(APIView):
    permission_classes = [IsManager | IsAdmin | IsBranchStaff]
    
    def get(self, request):
        try:
            person = Person.objects.select_subclasses().get(user=request.user)
            serializer = PersonSerializer(person)
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response({"error": "No se encontró un perfil de persona asociado a este usuario."}, status=status.HTTP_404_NOT_FOUND)


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
    permission_classes = [IsAdmin | IsManager]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


# RUD Retrieve - Update - Destroy
class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin |IsManager]
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class Branches(generics.ListAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = BranchSerializer
    
    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Branch.objects.filter(restaurant_id=restaurant_id)

# PRODUCTS
class Products(generics.ListAPIView):
    permission_classes = [ IsManager | IsAdmin | IsBranchStaff]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | IsManager | IsBranchStaff]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class Categories(generics.ListAPIView):
    permission_classes = [IsBranchStaff | IsManager | IsAdmin]
    serializer_class = CategorySerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Category.objects.filter(restaurant_id=restaurant_id)


class CategoryCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        restaurant_id = self.kwargs['restaurant_id']
        mutable_data = request.data.copy()
        mutable_data['restaurant'] = restaurant_id
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | IsManager | IsBranchStaff]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Category.objects.filter(restaurant_id=restaurant_id)


class CategoryExtraCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = CategoryExtraSerializer
    queryset = CategoryExtra.objects.all()


class CategoryExtraDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | IsManager]
    queryset = CategoryExtra.objects.all()
    serializer_class = CategoryExtraSerializer


class CategoriesExtra(generics.ListAPIView):
    permission_classes = [IsManager | IsAdmin]
    serializer_class = CategoryExtraSerializer
    queryset = CategoryExtra.objects.all()
        

# EMPLOYEES
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

class DailyOrders(generics.ListAPIView):
    permission_classes = [IsManager | IsAdmin]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        date = self.kwargs['date']
        return Order.objects.filter(created_at__date=date, branch_id=self.kwargs['branch_id'])
    
class DailyOrdersForRestaurant(generics.ListAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        date = self.kwargs['date']
        return Order.objects.filter(created_at__date=date, branch__restaurant_id=self.kwargs['restaurant_id'])
    

class Orders(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        if branch_id:
            return Order.objects.filter(branch_id=branch_id)
        return Order.objects.none()
    
    
class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    
class OrderCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        branch_id = self.kwargs.get('branch_id')
        if not branch_id:
            return Response({'error': 'Se requiere el ID de la sucursal'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(branch_id=branch_id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderItems(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    
class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class DeliveryOrderCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = DeliveryOrder.objects.all()
    serializer_class = DeliveryOrderSerializer


class DeliveryOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = DeliveryOrder.objects.all()
    serializer_class = DeliveryOrderSerializer


class TableOrderCreate(generics.CreateAPIView):
    permission_classes = [IsManager | IsBranchStaff | IsAdmin]
    queryset = TableOrder.objects.all()
    serializer_class = TableOrderSerializer

    def create(self, request, *args, **kwargs):
        branch_id = self.kwargs.get('branch_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(branch_id=branch_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TableOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = TableOrder.objects.all()
    serializer_class = TableOrderSerializer
    

class TableOrdersByTableView(generics.ListAPIView):
    """
    Vista para obtener todas las órdenes relacionadas con una mesa específica.
    """
    permission_classes = [AllowAny]
    serializer_class = TableOrderSerializer

    def get_queryset(self):
        table_id = self.kwargs['table_id']
        # Filtrar las órdenes para la mesa especificada
        orders = TableOrder.objects.filter(table__id=table_id)
        
        last_order = orders.last() if orders.exists() else None
        
        # Si hay una última orden, devolverla en un queryset; si no, devolver vacío
        return [last_order] if last_order else orders.none()


class TakeAwayOrderCreate(generics.CreateAPIView):
    permission_classes = [IsManager | IsBranchStaff | IsAdmin]
    queryset = TakeAwayOrder.objects.all()
    serializer_class = TakeAwayOrderSerializer

    def create(self, request, *args, **kwargs):
        branch_id = self.kwargs.get('branch_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(branch_id=branch_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
class TakeAwayOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = TakeAwayOrder.objects.all()
    serializer_class = TakeAwayOrderSerializer
    
    def perform_update(self, serializer):
        serializer.save()
        self.handle_ready_status(self.get_object())

    def handle_ready_status(self, new_order):
        if new_order.ready is True and new_order.phone_number is not None:
            notifyOrderReady(new_order)


class BranchStaffCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    queryset = BranchStaff.objects.all()
    serializer_class = BranchStaffSerializer

class BranchStaffs(generics.ListAPIView):
    permission_classes = [IsAdmin | IsManager]
    serializer_class = BranchStaffSerializer
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return BranchStaff.objects.filter(branch__restaurant_id=restaurant_id)

class BranchStaffList(generics.ListAPIView):
    permission_classes = [IsAdmin | IsManager | IsBranchStaff]
    serializer_class = BranchStaffListSerializer

    def get_queryset(self):
        branch_id = self.kwargs['branch_id']
        return BranchStaff.objects.filter(branch_id=branch_id)
    
class BranchStaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | IsManager]
    queryset = BranchStaff.objects.all()
    serializer_class = BranchStaffSerializer


# TABLES
class Tables(generics.ListAPIView):
    permission_classes = [IsManager | IsAdmin | IsBranchStaff]
    serializer_class = TableSerializer
    queryset = Table.objects.all()

    def get_queryset(self):
        branch_id = self.kwargs['branch_id']
        return Table.objects.filter(branch_id=branch_id)
    

class TableCreate(generics.CreateAPIView):
    permission_classes = [IsAdmin | IsManager]
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | IsManager]
    queryset = Table.objects.all()
    serializer_class = TableSerializer