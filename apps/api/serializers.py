from rest_framework import serializers
from apps.users.models import User
from apps.restaurant.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('name', 'website')


# class UserSerializer(serializers.ModelSerializer):
#     phone = serializers.CharField(default="")
#
#     class Meta:
#         model = User
#         fields = ('name', 'last_name', 'email', 'password', 'phone')
