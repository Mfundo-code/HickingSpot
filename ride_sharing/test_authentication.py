# tests/test_authentication.py

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

class UserRegistrationTest(APITestCase):

    def test_user_registration(self):
        url = reverse('register')  # Ensure this matches your URL configuration
        data = {
            'username': 'newuser',
            'password': 'password123',
            'phone_number': '0987654321'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
