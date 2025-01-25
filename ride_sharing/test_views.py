# tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ride_sharing.models import User, Driver

class DriverListViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='driver1',
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

    def test_get_driver_list(self):
        url = reverse('driver-list')  # Ensure this matches your URL configuration
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], 'driver1')
