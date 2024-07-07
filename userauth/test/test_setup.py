from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.organization_url = reverse('created-organisations')
        
        self.user_data = {
            'first_name':'rasheed',
            'last_name':'tiamiyu',
            'email':'rasheed@gmail.com',
            'password':'testing321',
            'phone':'09074833645',
        }
        
        self.login_data = {
            'email':'rasheed@gmail.com',
            'password':'testing321',
        }
        
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()