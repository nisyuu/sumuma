from django.test import TestCase
from django.contrib.auth import get_user_model
from kakeibo.models import Categories, KakeiboLabel
from shopping.forms import ToDoForm
import datetime

User = get_user_model()


class ShoppingFormsTests(TestCase):
    def setUp(self):
        """Set up user and category for form tests."""
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.expenditure_category = Categories.objects.create(
            name='Groceries',
            label=KakeiboLabel.EXPENDITURE,
            user=self.user
        )

    def test_todo_form_valid(self):
        """Test that the ToDoForm is valid with correct data."""
        form_data = {
            'name': 'Buy Bread',
            'amount': 200,
            'category': self.expenditure_category.pk,
            'event_date': datetime.date.today(),
            'memo': 'Sourdough bread',
            'is_bought': True,
            'is_registered': False,
        }
        form = ToDoForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_todo_form_minimal_valid(self):
        """Test that the ToDoForm is valid with only the required name field."""
        form_data = {
            'name': 'Get laundry detergent',
        }
        form = ToDoForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_todo_form_missing_name(self):
        """Test that the ToDoForm is invalid if the name is missing."""
        form_data = {
            'amount': 1000,
        }
        form = ToDoForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)