from django.test import TestCase, Client
from django.urls import reverse
from account.models import User


class AccountViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_get(self):
        """
        Test the login view page can be accessed.
        """
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
