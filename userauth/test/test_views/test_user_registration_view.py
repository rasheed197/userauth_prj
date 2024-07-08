# myapp/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from userauth.models import User, Organisation, UserOrganisation
import uuid
import bcrypt

class UserRegistrationViewTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_register_user_success(self):
        data = {
            'user_id': "john321",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "testing321",
            "phone": "+2347012345678"
        }

        response = self.client.post(self.register_url, data, format='json')
        
        # import pdb
        # pdb.set_trace()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Registration successful')
        # self.assertIn(response.data['data']['accessToken'], )
        self.assertEqual(response.data['data']['user']['firstName'], data['first_name'])
        self.assertEqual(response.data['data']['user']['lastName'], data['last_name'])
        self.assertEqual(response.data['data']['user']['email'], data['email'])
        self.assertEqual(response.data['data']['user']['phone'], data['phone'])

        # Check if the organisation is created
        user = User.objects.get(email=data['email'])
        self.assertTrue(Organisation.objects.filter(userorganisation__user=user).exists())

    def test_register_user_missing_fields(self):
        data = {
            "user_id": "john321",
            "first_name": "",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "testing321",
            "phone": "+2347012345678"
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Registration unsuccessful')

    def test_register_user_invalid_email(self):
        data = {
            'user_id': "john321",
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "testing321",
            "phone": "+2347012345678"
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Registration unsuccessful')

    def test_register_user_existing_email(self):
        # Create a user with the email
        User.objects.create(
            user_id='john321',
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            password='testing321'
        )

        data = {
            "user_id":"john123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "testing321",
            "phone": "+2347012345678"
        }

        response = self.client.post(self.register_url, data, format='json')
        
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Registration unsuccessful')



