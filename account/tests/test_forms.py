from django.test import TestCase
from unittest.mock import patch
from django_recaptcha.client import RecaptchaResponse
from account.forms import LoginForm
from account.models import User


class AccountFormsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')

    @patch("django_recaptcha.fields.client.submit")
    def test_login_form_valid(self, mock_submit):
        """
        Test the login form with valid data.
        """
        mock_submit.return_value = RecaptchaResponse(is_valid=True, extra_data={'score': 0.9})
        form_data = {'username': 'testuser@example.com', 'password': 'testpassword', 'recaptcha': 'dummy-value'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
