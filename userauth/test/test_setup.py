# from rest_framework.test import APITestCase
# from django.urls import reverse
# from userauth.models import User

# class TestSetUp(APITestCase):
    
#     def setUp(self):
        
#         self.register_url = reverse('register')
#         self.login_url = reverse('login')
#         self.created_organization_url = reverse('created-organisations')
#         self.organization_url = reverse('organisations')
#         self.user_own_record_url = f'api/users/{1}/'
        
        
#         self.user_data = {
#             'user_id':'rasheed197',
#             'first_name':'rasheed',
#             'last_name':'tiamiyu',
#             'email':'rasheed@gmail.com',
#             'password':'testing321',
#             'phone':'09074833645',
#         }
        
#         # self.user_own_record_url = reverse('get_user', kwargs={'id': self.user_data.id})
        
#         # # Create a user to get the id
#         # self.user = User.objects.save(**self.user_data)
#         # self.user_own_record_url = reverse(f'get_user/{1}')
#         # self.user_own_record_url = reverse('get_user', kwargs={'id': self.user.id})
        
#         # Create another user
#         self.other_user_data = {
#             'user_id':'testuser2',
#             'first_name':'Other',
#             'last_name':'User',
#             'email':'otheruser@example.com',
#             'password':'otherpassword123',
#             'phone':'+2349876543210'
#         }
        
#         self.organization_data = {
#             'org_id':'rasheed_org',
#             'name':'rasheed',
#             'description':'Rasheed Organisation!',
#         }
        
#         return super().setUp()
    
        
    
#     def tearDown(self):
#         return super().tearDown()