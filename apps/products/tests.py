from django.test import TestCase
from .models import Category, Product, CategoryExtra, ProductExtra
from apps.restaurant.models import Restaurant


class CategoryModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Product Restaurant',
            website='http://productrestaurant.com'
        )
        self.category = Category.objects.create(
            name='Appetizers',
            description='Starters',
            restaurant=self.restaurant
        )

    def test_category_creation(self):
        self.assertIsInstance(self.category, Category)
        self.assertEqual(self.category.name, 'Appetizers')
        self.assertEqual(self.category.restaurant, self.restaurant)
        self.assertEqual(str(self.category), 'Appetizers')


class ProductModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Product Restaurant',
            website='http://productrestaurant.com'
        )
        self.category = Category.objects.create(
            name='Main Course',
            description='Main Dishes',
            restaurant=self.restaurant
        )
        self.product = Product.objects.create(
            name='Grilled Chicken',
            description='Delicious grilled chicken',
            price=15.99,
            discount=0,
            category=self.category
        )

    def test_product_creation(self):
        self.assertIsInstance(self.product, Product)
        self.assertEqual(self.product.name, 'Grilled Chicken')
        self.assertEqual(self.product.price, 15.99)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(str(self.product), 'Grilled Chicken')


class CategoryExtraModelTest(TestCase):
    def setUp(self):
        self.category_extra = CategoryExtra.objects.create(
            name='Sauces',
            description='Extra sauces'
        )

    def test_category_extra_creation(self):
        self.assertIsInstance(self.category_extra, CategoryExtra)
        self.assertEqual(self.category_extra.name, 'Sauces')
        self.assertEqual(str(self.category_extra), 'Sauces')


class ProductExtraModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Burger',
            description='Beef burger',
            price=9.99
        )
        self.category_extra = CategoryExtra.objects.create(
            name='Cheeses',
            description='Different types of cheese'
        )
        self.product_extra = ProductExtra.objects.create(
            name='Cheddar Cheese',
            description='Extra cheddar',
            price=1.50,
            product=self.product,
            category=self.category_extra
        )

    def test_product_extra_creation(self):
        self.assertIsInstance(self.product_extra, ProductExtra)
        self.assertEqual(self.product_extra.name, 'Cheddar Cheese')
        self.assertEqual(self.product_extra.price, 1.50)
        self.assertEqual(self.product_extra.product, self.product)
        self.assertEqual(str(self.product_extra), 'Cheddar Cheese')
