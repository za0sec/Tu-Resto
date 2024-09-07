from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.orders.models import Order
from apps.users.models import User, Person, Manager, Waiter, Employee, Kitchen
from apps.restaurant.models import Restaurant, Table, Branch
from apps.products.models import Item


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'phone', 'started_at']


class RestaurantSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'website', 'employees')


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('number', 'capacity', 'branch', )


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'phone', 'restaurant')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','name', 'description', 'price')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ['user', 'phone', 'restaurant']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        manager = Manager.objects.create(user=user, **validated_data)
        return manager


class WaiterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Waiter
        fields = ['user', 'phone', 'restaurant']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        waiter = Waiter.objects.create(user=user, **validated_data)
        return waiter


class KitchenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Kitchen
        fields = ['user', 'phone', 'restaurant']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        kitchen = Kitchen.objects.create(user=user, **validated_data)
        return kitchen


class TuRestoTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            person = Person.objects.select_subclasses().get(user=user)

            token['first_name'] = person.user.first_name
            token['last_name'] = person.user.last_name
            token['email'] = person.user.email
            token['phone'] = person.phone

            token['role'] = person.__class__.__name__
        except Person.DoesNotExist:
            token['first_name'] = user.first_name
            token['last_name'] = user.last_name
            token['email'] = user.email
            token['role'] = 'Unknown'

        return token
