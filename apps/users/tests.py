from django.test import TestCase
from django.contrib.auth.models import User
from .models import Person, Employee, BranchStaff, Waiter, Cashier, Kitchen, Manager, Admin
from apps.restaurant.models import Restaurant, Branch


class PersonModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='personuser', password='testpassword')
        self.person = Person.objects.create(user=self.user, phone='000111222')

    def test_person_creation(self):
        self.assertIsInstance(self.person, Person)
        self.assertEqual(self.person.user.username, 'personuser')
        self.assertEqual(str(self.person), 'personuser')


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employeeuser', password='testpassword')
        self.employee = Employee.objects.create(user=self.user, phone='333444555')

    def test_employee_creation(self):
        self.assertIsInstance(self.employee, Employee)
        self.assertEqual(self.employee.user.username, 'employeeuser')


class BranchStaffModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='branchstaffuser', password='testpassword')
        self.branch = Branch.objects.create(
            name='Staff Branch',
            address='789 Staff St',
            phone='555-555-7777',
            restaurant=Restaurant.objects.create(name='Staff Restaurant', website='http://staffrestaurant.com')
        )
        self.branch_staff = BranchStaff.objects.create(user=self.user, phone='666777888', branch=self.branch)

    def test_branch_staff_creation(self):
        self.assertIsInstance(self.branch_staff, BranchStaff)
        self.assertEqual(self.branch_staff.user.username, 'branchstaffuser')
        self.assertEqual(self.branch_staff.branch, self.branch)


class WaiterModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='waiteruser', password='testpassword')
        self.waiter = Waiter.objects.create(user=self.user, phone='999000111')

    def test_waiter_creation(self):
        self.assertIsInstance(self.waiter, Waiter)
        self.assertEqual(self.waiter.user.username, 'waiteruser')


class CashierModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cashieruser', password='testpassword')
        self.cashier = Cashier.objects.create(user=self.user, phone='222333444')

    def test_cashier_creation(self):
        self.assertIsInstance(self.cashier, Cashier)
        self.assertEqual(self.cashier.user.username, 'cashieruser')


class KitchenModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kitchenuser', password='testpassword')
        self.kitchen_staff = Kitchen.objects.create(user=self.user, phone='555666777')

    def test_kitchen_staff_creation(self):
        self.assertIsInstance(self.kitchen_staff, Kitchen)
        self.assertEqual(self.kitchen_staff.user.username, 'kitchenuser')


class ManagerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='manageruser', password='testpassword')
        self.restaurant = Restaurant.objects.create(name='Manager Restaurant', website='http://managerrestaurant.com')
        self.manager = Manager.objects.create(user=self.user, phone='888999000', restaurant=self.restaurant)

    def test_manager_creation(self):
        self.assertIsInstance(self.manager, Manager)
        self.assertEqual(self.manager.user.username, 'manageruser')
        self.assertEqual(self.manager.restaurant, self.restaurant)


class AdminModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='adminuser', password='testpassword')
        self.admin = Admin.objects.create(user=self.user, phone='123123123')

    def test_admin_creation(self):
        self.assertIsInstance(self.admin, Admin)
        self.assertEqual(self.admin.user.username, 'adminuser')
