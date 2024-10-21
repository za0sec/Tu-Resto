from django.test import TestCase
from .models import Order, OrderItem, TableOrder, DeliveryOrder, TakeAwayOrder
from apps.restaurant.models import Restaurant, Branch, Table
from apps.products.models import Product, ProductExtra
from apps.users.models import BranchStaff
from django.contrib.auth.models import User


class OrderModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Order Restaurant', website='http://orderrestaurant.com')
        self.branch = Branch.objects.create(
            name='Order Branch',
            address='123 Order St',
            phone='555-555-8888',
            restaurant=self.restaurant
        )
        self.user = User.objects.create_user(username='orderstaff', password='testpassword')
        self.branch_staff = BranchStaff.objects.create(user=self.user, phone='777888999', branch=self.branch)
        self.order = Order.objects.create(
            branch=self.branch,
            paid=False,
            delivered=False,
            branch_staff=self.branch_staff
        )

    def test_order_creation(self):
        self.assertIsInstance(self.order, Order)
        self.assertEqual(self.order.branch, self.branch)
        self.assertEqual(self.order.paid, False)
        self.assertEqual(self.order.branch_staff, self.branch_staff)
        self.assertEqual(str(self.order), f"Order {self.order.id} - {self.order.created_at.date()}")

    def test_order_total(self):
        product = Product.objects.create(name='Test Product', price=10.00)
        order_item = OrderItem.objects.create(order=self.order, product=product, quantity=2)
        self.assertEqual(self.order.get_total(), 20.00)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(branch=Branch.objects.create(
            name='Item Branch',
            address='456 Item St',
            phone='555-555-9999',
            restaurant=Restaurant.objects.create(name='Item Restaurant', website='http://itemrestaurant.com')
        ))
        self.product = Product.objects.create(name='Item Product', price=5.00)
        self.product_extra = ProductExtra.objects.create(name='Extra Item', price=1.00, product=self.product)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=3)
        self.order_item.extras.add(self.product_extra)

    def test_order_item_creation(self):
        self.assertIsInstance(self.order_item, OrderItem)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 3)
        self.assertEqual(str(self.order_item), f"Order {self.order.id} - {self.product.name} x {self.order_item.quantity}")

class TableOrderModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='TableOrder Restaurant', website='http://tableorderrestaurant.com')
        self.branch = Branch.objects.create(
            name='TableOrder Branch',
            address='789 TableOrder St',
            phone='555-555-0000',
            restaurant=self.restaurant
        )
        self.table = Table.objects.create(number=1, capacity=4, position_x=10, position_y=20, branch=self.branch)
        self.table_order = TableOrder.objects.create(
            branch=self.branch,
            table=self.table,
            status_closed=False
        )

    def test_table_order_creation(self):
        self.assertIsInstance(self.table_order, TableOrder)
        self.assertEqual(self.table_order.table, self.table)
        self.assertEqual(self.table_order.status_closed, False)
        self.assertEqual(str(self.table_order), f"Table {self.table.number} Order {self.table_order.id}")


class DeliveryOrderModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Delivery Restaurant', website='http://deliveryrestaurant.com')
        self.branch = Branch.objects.create(
            name='Delivery Branch',
            address='101 Delivery St',
            phone='555-555-1111',
            restaurant=self.restaurant
        )
        self.delivery_order = DeliveryOrder.objects.create(
            branch=self.branch,
            address='123 Customer St',
            phone_number='555-1234',
            ready=False
        )

    def test_delivery_order_creation(self):
        self.assertIsInstance(self.delivery_order, DeliveryOrder)
        self.assertEqual(self.delivery_order.address, '123 Customer St')
        self.assertEqual(self.delivery_order.ready, False)
        self.assertEqual(str(self.delivery_order), f"Delivery Order {self.delivery_order.id} at {self.delivery_order.address}")


class TakeAwayOrderModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='TakeAway Restaurant', website='http://takeawayrestaurant.com')
        self.branch = Branch.objects.create(
            name='TakeAway Branch',
            address='202 TakeAway St',
            phone='555-555-2222',
            restaurant=self.restaurant
        )
        self.takeaway_order = TakeAwayOrder.objects.create(
            branch=self.branch,
            phone_number='555-5678',
            ready=False
        )

    def test_takeaway_order_creation(self):
        self.assertIsInstance(self.takeaway_order, TakeAwayOrder)
        self.assertEqual(self.takeaway_order.phone_number, '555-5678')
        self.assertEqual(self.takeaway_order.ready, False)
        self.assertEqual(str(self.takeaway_order), f"Take Away Order {self.takeaway_order.id}")
