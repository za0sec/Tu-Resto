from django.test import TestCase
import unittest
from .models import Restaurant, Branch, Table
from apps.users.models import Employee, BranchStaff, Person, Waiter, Cashier, Kitchen, Manager
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RestaurantModelTest(TestCase):
    def test_restaurant_creation(self):
        restaurant = Restaurant.objects.create(name="Testaurant", website="http://testaurant.com")
        self.assertEqual(restaurant.name, "Testaurant")
        self.assertEqual(restaurant.website, "http://testaurant.com")
        self.assertIsNotNone(restaurant.created_at)
        self.assertIsNotNone(restaurant.updated_at)
        self.assertEqual(str(restaurant), "Testaurant")

class BranchModelTest(TestCase):
    def test_branch_creation(self):
        restaurant = Restaurant.objects.create(name="Testaurant", website="http://testaurant.com")
        user = User.objects.create(first_name="John", last_name="Doe", username="johndoe", email="hola@gmail.com")
        employee = Employee.objects.create(user=user)
        branch = Branch.objects.create(name="Main Branch", address="123 Test St", phone="123-456-7890", restaurant=restaurant, employees=employee)
        self.assertEqual(branch.name, "Main Branch")
        self.assertEqual(branch.address, "123 Test St")
        self.assertEqual(branch.phone, "123-456-7890")
        self.assertEqual(branch.restaurant, restaurant)
        self.assertEqual(branch.employees, employee)
        self.assertIsNotNone(branch.created_at)
        self.assertIsNotNone(branch.updated_at)

class TableModelTest(TestCase):
    def test_table_creation(self):
        restaurant = Restaurant.objects.create(name="Testaurant", website="http://testaurant.com")
        branch = Branch.objects.create(name="Main Branch", address="123 Test St", phone="123-456-7890", restaurant=restaurant)
        branchStaff = BranchStaff.objects.create(name="Jane Doe", branch=branch)  # Adjust based on actual Waiter model 
        table = Table.objects.create(number=1, capacity=4, branch=branch, waiter=branchStaff)
        self.assertEqual(table.number, 1)
        self.assertEqual(table.capacity, 4)
        self.assertEqual(table.branch, branch)
        self.assertEqual(table.waiter, branchStaff)
        self.assertEqual(str(table), f"Table 1 at {branch.name}")

class TableModelTest(TestCase):
    def test_table_creation(self):
        #todo
        pass
        
    def test_table_creation_without_number(self):
        #todo
        pass

    def test_table_creation_without_capacity(self):
        #todo
        pass

    def test_table_creation_without_branch(self):
        #todo
        pass

class EmployeeModelTest(TestCase):
    def test_employee_creation_without_name(self):
        user = User.objects.create(username='testuser')  # Crear un usuario de prueba
        
        with self.assertRaises(ValidationError):
            employee = Employee.objects.create(user=user)  # Pasar el user_id requerido
            employee.full_clean()  # Este método dispara la validación


from django.test import TestCase
from django.contrib.auth.models import User
from .models import Restaurant, Branch, Table
from apps.users.models import Employee, Waiter


class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            website='http://testrestaurant.com'
        )

    def test_restaurant_creation(self):
        self.assertIsInstance(self.restaurant, Restaurant)
        self.assertEqual(self.restaurant.name, 'Test Restaurant')
        self.assertEqual(self.restaurant.website, 'http://testrestaurant.com')
        self.assertEqual(str(self.restaurant), 'Test Restaurant')

    def test_restaurant_unique_name(self):
        with self.assertRaises(Exception):
            Restaurant.objects.create(
                name='Test Restaurant',
                website='http://anotherwebsite.com'
            )


class BranchModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Branch Restaurant',
            website='http://branchrestaurant.com'
        )
        self.user = User.objects.create_user(username='employee', password='testpassword')
        self.employee = Employee.objects.create(user=self.user, phone='123456789')
        self.branch = Branch.objects.create(
            name='Main Branch',
            address='123 Main St',
            phone='555-555-5555',
            restaurant=self.restaurant,
            employees=self.employee
        )

    def test_branch_creation(self):
        self.assertIsInstance(self.branch, Branch)
        self.assertEqual(self.branch.name, 'Main Branch')
        self.assertEqual(self.branch.address, '123 Main St')
        self.assertEqual(self.branch.restaurant, self.restaurant)
        self.assertEqual(self.branch.employees, self.employee)
        self.assertEqual(str(self.branch), 'Main Branch at 123 Main St')

    def test_branch_unique_constraint(self):
        with self.assertRaises(Exception):
            Branch.objects.create(
                name='Main Branch',
                address='123 Main St',
                phone='555-555-0000',
                restaurant=self.restaurant,
                employees=self.employee
            )


class TableModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Table Restaurant',
            website='http://tablerestaurant.com'
        )
        self.user = User.objects.create_user(username='waiter', password='testpassword')
        self.waiter = Waiter.objects.create(user=self.user, phone='987654321')
        self.branch = Branch.objects.create(
            name='Table Branch',
            address='456 Table St',
            phone='555-555-6666',
            restaurant=self.restaurant,
            employees=self.waiter
        )
        self.table = Table.objects.create(
            number=1,
            capacity=4,
            position_x=10,
            position_y=20,
            bookable=True,
            branch=self.branch,
            waiter=self.waiter
        )

    def test_table_creation(self):
        self.assertIsInstance(self.table, Table)
        self.assertEqual(self.table.number, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertEqual(self.table.branch, self.branch)
        self.assertEqual(self.table.waiter, self.waiter)
        self.assertEqual(str(self.table), 'Table 1 at Table Branch')

    def test_table_unique_number_per_branch(self):
        with self.assertRaises(Exception):
            Table.objects.create(
                number=1,
                capacity=2,
                position_x=15,
                position_y=25,
                bookable=False,
                branch=self.branch,
                waiter=self.waiter
            )

    def test_table_unique_position_per_branch(self):
        with self.assertRaises(Exception):
            Table.objects.create(
                number=2,
                capacity=2,
                position_x=10,
                position_y=20,
                bookable=False,
                branch=self.branch,
                waiter=self.waiter
            )
