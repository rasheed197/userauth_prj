from .test_setup import TestSetUp

class TestViews(TestSetUp):
    
    def test_user_cannot_register_with_no_data(self):
        res=self.client.post(self.register_url)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, 400)
        
    def test_user_can_register_succesfully(self):
        res=self.client.post(
            self.register_url, self.user_data, format="json")
        
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, 201)
        
    def test_user_cannot_login_without_email_and_password(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        res=self.client.post(self.login_url, format="json")
        
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, 401)
        
    def test_user_can_login_with_email_and_password(self):
        self.client.post(
            self.register_url, self.user_data, format="json")
        res=self.client.post(self.login_url, self.user_data, format="json")
        
        import pdb
        pdb.set_trace()
        self.assertEqual(res.status_code, 200)