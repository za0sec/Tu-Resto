from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from apps.orders.models import Order
from apps.users.models import User, Person, Manager, Waiter, Employee, Kitchen
from apps.restaurant.models import Restaurant, Table, Branch
from apps.orders.models import Order, TakeAwayOrder, TableOrder, DeliveryOrder, OrderItem
from apps.products.models import Product, ProductExtra, Category, CategoryExtra
from apps.subscription.models import Plan, Subscription
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail


from django.conf import settings

# Subscription

class PlanSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = '__all__'

    def get_features(self, obj):
        features = obj.features.all()
        return [feature.name for feature in features]
    
class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'is_active']

    


# USERS

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['user', 'phone', 'started_at', 'branch']


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

# RESTAURANTS

class RestaurantSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    subscriptions = SubscriptionSerializer(read_only=True)
    banner = serializers.SerializerMethodField()

    def get_banner(self, obj):
        if obj.banner:
            return settings.PAGE_URL + obj.banner.url
        return None

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'website', 'employees', 'banner', 'subscriptions')

    def create(self, validated_data):
        banner = validated_data.pop('banner', None)
        restaurant = Restaurant.objects.create(**validated_data)
        if banner:
            restaurant.banner = banner
            restaurant.save()
        return restaurant

    def update(self, instance, validated_data):
        banner = validated_data.pop('banner', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if banner:
            instance.banner = banner
        instance.save()
        return instance
    



# TABLES
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('number', 'capacity', 'branch' )


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'phone', 'restaurant')


class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), write_only=True)

    class Meta:
        model = Manager
        fields = ['user', 'phone', 'restaurant', 'branch']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['restaurant'] = RestaurantSerializer(instance.restaurant).data
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        restaurant = validated_data.pop('restaurant')
        user = User.objects.create_user(**user_data)
        manager = Manager.objects.create(user=user, restaurant=restaurant, **validated_data)

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"{settings.FRONTEND_URL}/reset-password?uidb64={uidb64}&token={token}"

        self.send_password_reset_email(user.email, reset_url)

        return manager

    def send_password_reset_email(self, email, reset_url):
        subject = "Crea tu contraseña"
        message = f"Por favor, haz clic en el siguiente enlace para crear tu contraseña: {reset_url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


# PRODUCTS

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductExtra
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExtra
        fields = '__all__'

# PERSON SERIALIZERS

class PersonSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        person = Person.objects.select_subclasses().get(pk=instance.pk)
        role = person.__class__.__name__
        serializer_class = globals().get(f"{role}Serializer")
        
        if serializer_class:
            return serializer_class(person).data
        else:
            return super().to_representation(instance)

    class Meta:
        model = Person
        fields = '__all__'




# TOKENS

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

# ORDERS

class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.get_total()
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class TakeAwayOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakeAwayOrder
        fields = '__all__'

class TableOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableOrder
        fields = '__all__'

class DeliveryOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryOrder
        fields =  '__all__'
