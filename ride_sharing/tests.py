#test.py
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Driver, User

class DriverModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.driver = Driver.objects.create(
            user=self.user,
            license_number="ABC12345",
            vehicle_details="Sedan, White, 2019",
            available_seats=4,
            is_available=True
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.user.username, "johndoe")
        self.assertEqual(self.driver.license_number, "ABC12345")

class DriverAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.driver = Driver.objects.create(
            user=self.user,
            license_number="ABC12345",
            vehicle_details="Sedan, White, 2019",
            available_seats=4,
            is_available=True
        )

    def test_get_drivers(self):
        url = reverse('driver-list')  # Ensure the URL name matches your URL configuration
        response = self.client.get(url)
        print(response.data)  # Add this line to print the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], "johndoe")


