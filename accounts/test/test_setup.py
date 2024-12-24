from rest_framework.test import APITestCase,APIClient
from django.urls import reverse


class TestSetup(APITestCase):
    def setUp(self):
        account_url='/auth'
        self.register_url =account_url+'/account/'
        self.login_url = account_url+'/login/'
        
        self.user_data = {
            "telephone": "+250728444282",
            "first_name": "Jambo",
            "last_name": "Florbert",
            "password": "Habimana97",
            "user_type":"END_USER"
            }
        self.login_with_email_data = {
            "username": "+250728444282",
            "password": "Habimana97",
        }
      
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
