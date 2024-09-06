from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.orders.models import Order
from apps.users.models import User, Person
from apps.restaurant.models import Restaurant,Table,Branch
from apps.products.models import Item

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'website')


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('number', 'capacity', 'branch', )


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id','name', 'address', 'phone', 'restaurant')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','name', 'description', 'price')



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        try:
            person = Person.objects.get(user=user)
            token['first_name'] = person.user.first_name
            token['last_name'] = person.user.last_name
            token['email'] = person.user.email
            token['phone'] = person.phone
        except Person.DoesNotExist:
            token['first_name'] = user.first_name
            token['last_name'] = user.last_name
            token['email'] = user.email

        return token

