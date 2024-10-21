from django.test import TestCase
from .models import Plan, Subscription, SubscriptionFeature
from apps.restaurant.models import Restaurant
from datetime import datetime, timedelta


class PlanModelTest(TestCase):
    def setUp(self):
        self.plan = Plan.objects.create(
            name='Premium Plan',
            description='Access to premium features',
            price=49.99,
            duration_days=30
        )

    def test_plan_creation(self):
        self.assertIsInstance(self.plan, Plan)
        self.assertEqual(self.plan.name, 'Premium Plan')
        self.assertEqual(str(self.plan), 'Premium Plan')


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Subscribed Restaurant',
            website='http://subscribedrestaurant.com'
        )
        self.plan = Plan.objects.create(
            name='Basic Plan',
            description='Access to basic features',
            price=19.99,
            duration_days=30
        )
        self.subscription = Subscription.objects.create(
            restaurant=self.restaurant,
            plan=self.plan,
            end_date=datetime.now() + timedelta(days=self.plan.duration_days)
        )

    def test_subscription_creation(self):
        self.assertIsInstance(self.subscription, Subscription)
        self.assertEqual(self.subscription.restaurant, self.restaurant)
        self.assertEqual(self.subscription.plan, self.plan)
        self.assertEqual(self.subscription.is_active, True)
        self.assertEqual(str(self.subscription), f"{self.restaurant.name} - {self.plan.name}")


class SubscriptionFeatureModelTest(TestCase):
    def setUp(self):
        self.plan = Plan.objects.create(
            name='Advanced Plan',
            description='Access to advanced features',
            price=29.99,
            duration_days=30
        )
        self.feature = SubscriptionFeature.objects.create(
            plan=self.plan,
            name='Priority Support',
            description='Get priority customer support'
        )

    def test_subscription_feature_creation(self):
        self.assertIsInstance(self.feature, SubscriptionFeature)
        self.assertEqual(self.feature.plan, self.plan)
        self.assertEqual(str(self.feature), f"{self.plan.name} - {self.feature.name}")
