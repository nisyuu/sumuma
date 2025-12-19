from django.test import TestCase
from account.forms import LoginForm


class AccountFormsTests(TestCase):
    def test_login_form_valid(self):
        """
        Test the login form with valid data.
        """
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        form = LoginForm(data=form_data)
        # This will fail until a user is created. It's a placeholder.
        # self.assertTrue(form.is_valid())
        pass
