from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from userauth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt
import uuid

class UserDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for testing
        self.user = User.objects.create(
            user_id='john123',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password=bcrypt.hashpw('testing321'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone='+2347012345678'
        )
        self.login_url = reverse('login')  # Assuming you have a login view
        self.url = reverse('user_detail', kwargs={'id': self.user.id})

    def authenticate(self):
        login_response = self.client.post(self.login_url, {
            'email': 'john@example.com',
            'password': 'testing321'
        })
        print('Login Response:', login_response.data)
        
        if 'accessToken' in login_response.data['data']:
            token = login_response.data['data']['accessToken']
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        else:
            print("Authentication failed. No token returned.")
            raise Exception("Authentication failed. No token returned.")

    def test_get_user_detail_success(self):
        self.authenticate()
        response = self.client.get(self.url)
        
        # Print the response for debugging
        print('User Detail Response:', response.data)  
        
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['userId'], self.user.user_id)
        self.assertEqual(response.data['data']['firstName'], self.user.first_name)
        self.assertEqual(response.data['data']['lastName'], self.user.last_name)
        self.assertEqual(response.data['data']['email'], self.user.email)
        self.assertEqual(response.data['data']['phone'], self.user.phone)

    def test_get_user_detail_unauthenticated(self):
        self.client.credentials()  # Remove authentication credentials
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

# Run the tests
if __name__ == '__main__':
    import unittest
    unittest.main()
