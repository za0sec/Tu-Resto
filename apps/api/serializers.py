from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from apps.orders.models import Order
from apps.users.models import User, Person, Manager, Waiter, Employee, Kitchen, BranchStaff
from apps.restaurant.models import Restaurant, Table, Branch
from apps.orders.models import Order, TakeAwayOrder, TableOrder, DeliveryOrder, OrderItem
from apps.products.models import Product, ProductExtra, Category, CategoryExtra
from apps.subscription.models import Plan, Subscription
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import models

import json

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


# TABLES
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


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
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = ProductSerializer(instance.product_set.all(), many=True).data
        return representation



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

            if isinstance(person, Manager) or isinstance(person, BranchStaff):
                token['restaurant_id'] = person.restaurant.id if hasattr(person, 'restaurant') and person.restaurant else (person.branch.restaurant.id if hasattr(person, 'branch') and person.branch else None)
            if isinstance(person, BranchStaff):
                token['branch_id'] = person.branch.id if person.branch else None

        except Person.DoesNotExist:
            token['first_name'] = user.first_name
            token['last_name'] = user.last_name
            token['email'] = user.email
            token['role'] = 'Unknown'

        return token

# ORDERS


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    extras = serializers.PrimaryKeyRelatedField(many=True, queryset=ProductExtra.objects.all())

    class Meta:
        model = OrderItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        representation['extras'] = ProductExtraSerializer(instance.extras.all(), many=True).data
        return representation


class TakeAwayOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    branch_staff = serializers.PrimaryKeyRelatedField(queryset=BranchStaff.objects.all(), allow_null=True, required=False)

    class Meta:
        model = TakeAwayOrder
        fields = ['id', 'phone_number', 'branch_staff', 'ready', 'payment_method', 'commentary', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        branch_staff_id = validated_data.pop('branch_staff', None)

        if branch_staff_id:
            branch_staff = BranchStaff.objects.get(id=branch_staff_id.id)   
            validated_data['branch_staff'] = branch_staff

        takeaway_order = TakeAwayOrder.objects.create(**validated_data)

        if order_items_data:
            for order_item_data in order_items_data:
                product = order_item_data.get('product')
                extras = order_item_data.pop('extras', [])
                order_item = OrderItem.objects.create(
                    order=takeaway_order,
                    product=product,
                    quantity=order_item_data.get('quantity'),
                    commentary=order_item_data.get('commentary')
                )
                order_item.extras.set(extras)

        return takeaway_order

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.branch_staff = validated_data.get('branch_staff', instance.branch_staff)
        instance.ready = validated_data.get('ready', instance.ready)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.commentary = validated_data.get('commentary', instance.commentary)
        instance.save()

        order_items_data = validated_data.pop('order_items', None)

        if order_items_data is not None:
            instance.order_items.all().delete()
            for order_item_data in order_items_data:
                product = order_item_data.get('product')
                extras = order_item_data.pop('extras', [])
                order_item = OrderItem.objects.create(
                    order=instance,
                    product=product,
                    quantity=order_item_data.get('quantity'),
                    commentary=order_item_data.get('commentary')
                )
                order_item.extras.set(extras)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['branch_staff'] = BranchStaffSerializer(instance.branch_staff).data if instance.branch_staff else None
        representation['order_items'] = OrderItemSerializer(instance.order_items.all(), many=True).data
        return representation


class TableOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    branch_staff = serializers.PrimaryKeyRelatedField(queryset=BranchStaff.objects.all(), allow_null=True, required=False)

    class Meta:
        model = TableOrder
        fields = ['id', 'table', 'branch_staff', 'status_closed', 'payment_method', 'commentary', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        branch_staff_id = validated_data.pop('branch_staff', None)

        if branch_staff_id:
            branch_staff = BranchStaff.objects.get(id=branch_staff_id.id)   
            validated_data['branch_staff'] = branch_staff

        table_order = TableOrder.objects.create(**validated_data)

        if order_items_data:
            for order_item_data in order_items_data:
                product = order_item_data.get('product')
                extras = order_item_data.pop('extras', [])
                order_item = OrderItem.objects.create(
                    order=table_order,
                    product=product,
                    quantity=order_item_data.get('quantity'),
                    commentary=order_item_data.get('commentary')
                )
                order_item.extras.set(extras)

        return table_order

    def update(self, instance, validated_data):
        instance.table = validated_data.get('table', instance.table)
        instance.branch_staff = validated_data.get('branch_staff', instance.branch_staff)
        instance.status_closed = validated_data.get('status_closed', instance.status_closed)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.commentary = validated_data.get('commentary', instance.commentary)
        instance.save()

        order_items_data = validated_data.pop('order_items', None)

        if order_items_data is not None:
            instance.order_items.all().delete()
            for order_item_data in order_items_data:
                product = order_item_data.get('product')
                extras = order_item_data.pop('extras', [])
                order_item = OrderItem.objects.create(
                    order=instance,
                    product=product,
                    quantity=order_item_data.get('quantity'),
                    commentary=order_item_data.get('commentary')
                )
                order_item.extras.set(extras)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['branch_staff'] = BranchStaffSerializer(instance.branch_staff).data if instance.branch_staff else None
        representation['order_items'] = OrderItemSerializer(instance.order_items.all(), many=True).data
        return representation

class DeliveryOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryOrder
        fields =  '__all__'

class BranchStaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), write_only=True)

    class Meta:
        model = BranchStaff
        fields = ['user', 'phone', 'branch']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['branch'] = BranchSerializer(instance.branch).data
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        branch = validated_data.pop('branch')
        user = User.objects.create_user(**user_data)
        branch_staff = BranchStaff.objects.create(user=user, branch=branch, **validated_data)

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"{settings.FRONTEND_URL}/reset-password?uidb64={uidb64}&token={token}"

        self.send_password_reset_email(user.email, reset_url)

        return branch_staff

    def send_password_reset_email(self, email, reset_url):
        subject = "Crea tu contraseña"
        message = f"Por favor, haz clic en el siguiente enlace para crear tu contraseña: {reset_url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


class BranchStaffListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BranchStaff
        fields = ['id', 'user', 'phone', 'branch']


class BranchSerializer(serializers.ModelSerializer):
    branch_employees = EmployeeSerializer(many=True, read_only=True)
    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'phone', 'restaurant', 'branch_employees')


class RestaurantSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()
    subscriptions = SubscriptionSerializer(read_only=True)
    banner = serializers.SerializerMethodField()
    branches = serializers.SerializerMethodField()

    def get_branches(self, obj):
        return Branch.objects.filter(restaurant=obj).count()

    def get_banner(self, obj):
        if obj.banner:
            return settings.PAGE_URL + obj.banner.url
        return None
    
    def get_employees(self, obj):
        return Employee.objects.filter(branch__restaurant=obj).count()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'website', 'employees', 'banner', 'subscriptions', 'branches')

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
    
class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    branch_staff = BranchStaffSerializer()
    order_type = serializers.SerializerMethodField()
    table = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.get_total()
    
    def get_items(self, obj):
        return OrderItemSerializer(obj.order_items.all(), many=True).data
    
    def get_order_type(self, obj):
        return Order.objects.get_subclass(id=obj.id).__class__.__name__
    
    def get_table(self, obj):
        order_subclass = Order.objects.get_subclass(id=obj.id)
        if isinstance(order_subclass, TableOrder):
            return TableSerializer(order_subclass.table).data
        return None
    
    class Meta:
        model = Order
        fields = '__all__'
