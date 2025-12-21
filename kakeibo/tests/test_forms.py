import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from kakeibo.models import Categories, KakeiboLabel
from kakeibo.forms import IncomeForm, ExpenditureForm, CategoryForm

User = get_user_model()


class KakeiboFormsTests(TestCase):

    def setUp(self):
        """Set up data for form tests."""
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.income_category = Categories.objects.create(
            name='Salary',
            label=KakeiboLabel.INCOME,
            user=self.user
        )
        self.expenditure_category = Categories.objects.create(
            name='Groceries',
            label=KakeiboLabel.EXPENDITURE,
            user=self.user
        )

    def test_income_form_valid(self):
        """Test that the IncomeForm is valid with correct data."""
        form_data = {
            'amount': 50000,
            'category': self.income_category.pk,
            'event_date': datetime.date.today(),
            'memo': 'Test income memo'
        }
        form = IncomeForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_income_form_invalid_category(self):
        """Test that the IncomeForm is invalid if an expenditure category is used."""
        form_data = {
            'amount': 50000,
            'category': self.expenditure_category.pk, # Wrong category type
            'event_date': datetime.date.today(),
        }
        form = IncomeForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_expenditure_form_valid(self):
        """Test that the ExpenditureForm is valid with correct data."""
        form_data = {
            'amount': 3000,
            'category': self.expenditure_category.pk,
            'event_date': datetime.date.today(),
            'memo': 'Test expenditure memo'
        }
        form = ExpenditureForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_expenditure_form_invalid_category(self):
        """Test that the ExpenditureForm is invalid if an income category is used."""
        form_data = {
            'amount': 3000,
            'category': self.income_category.pk, # Wrong category type
            'event_date': datetime.date.today(),
        }
        form = ExpenditureForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_category_form_valid(self):
        """Test that the CategoryForm is valid with correct data."""
        form_data = {
            'name': 'New Category',
            'label': KakeiboLabel.INCOME
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_name_too_long(self):
        """Test that the CategoryForm is invalid if the name is too long."""
        form_data = {
            'name': 'a' * 33, # Max length is 32
            'label': KakeiboLabel.EXPENDITURE
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)