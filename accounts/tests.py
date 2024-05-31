from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import StoreUser

class AccountsTests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('signup_Api')
        self.login_url = reverse('login_Api')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'username': 'testuser'
        }
        self.user = StoreUser.objects.create_user(**self.user_data)

    def test_user_signup(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'username': 'newuser'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Token', response.data)
        self.assertIn('user', response.data)

    def test_user_signup_existing_email(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_226_IM_USED)

    def test_user_login(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Token', response.data)
        self.assertIn('user', response.data)

    def test_user_login_invalid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)