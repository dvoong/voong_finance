from django.test import TestCase
from django.urls import resolve
from .views import initialise_balance

# Create your tests here.
class MyTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):

        resolver = resolve('/api/initialise-balance')
        self.assertEqual(resolver.func, initialise_balance)
