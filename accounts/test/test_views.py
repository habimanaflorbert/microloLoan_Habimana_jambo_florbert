from django.urls import reverse
from accounts.test.test_setup import TestSetup
from django.contrib.auth import get_user_model
# from accounts.models import ResetPhoneOTP

User = get_user_model()


class TestAccountsViews(TestSetup):
    def authenticate(self):
        reg_res = self.client.post(
            self.register_url, self.user_data, format="json")
        self.assertEqual(reg_res.status_code, 201)
        username = reg_res.data['telephone']
        user = User.objects.get(telephone=username)
        user.is_active = True
        user.save()
        login_res = self.client.post(
            self.login_url, self.user_data, format="json")
        self.assertEqual(login_res.status_code, 200)
        jwt_token = 'JWT '+login_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=jwt_token)
    