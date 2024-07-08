from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from userauth.models import User
import bcrypt
import uuid


class UserLoginViewTest(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        # Create a user for testing login
        self.user = User.objects.create(
            user_id='john321',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password=bcrypt.hashpw('testing321'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone='+2347012345678'
        )

    def test_login_user_success(self):
        data = {
            "email": "john@example.com",
            "password": "testing321"
        }

        response = self.client.post(self.login_url, data, format='json')
        
        # import pdb
        # pdb.set_trace()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Login successful')
        self.assertEqual(response.data['data']['user']['userId'], self.user.user_id)
        self.assertEqual(response.data['data']['user']['firstName'], self.user.first_name)
        self.assertEqual(response.data['data']['user']['lastName'], self.user.last_name)
        self.assertEqual(response.data['data']['user']['email'], self.user.email)
        self.assertEqual(response.data['data']['user']['phone'], self.user.phone)

    def test_login_user_invalid_credentials(self):
        data = {
            "email": "john@example.com",
            "password": "wrongpassword"
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Authentication failed')
        self.assertEqual(response.data['statusCode'], 401)

    def test_login_user_nonexistent_email(self):
        data = {
            "email": "nonexistent@example.com",
            "password": "testing321"
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Authentication failed')
        self.assertEqual(response.data['statusCode'], 401)