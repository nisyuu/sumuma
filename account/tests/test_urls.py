from django.test import TestCase
from django.urls import reverse, resolve
from account.views import Login, Logout


class AccountUrlsTests(TestCase):
    def test_login_url_resolves(self):
        """
        Test that the login url resolves to the login view.
        """
        url = reverse('account:login')
        self.assertEqual(resolve(url).func.view_class, Login)
