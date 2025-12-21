from django.test import TestCase
from django.db.models import ProtectedError
from django.contrib.auth import get_user_model
from kakeibo.models import Categories, Incomes, Expenditures, KakeiboLabel

User = get_user_model()


class KakeiboModelTests(TestCase):
    def setUp(self):
        """Create a user for all tests in this class."""
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')

    def test_create_category(self):
        """Test creating a category."""
        category = Categories.objects.create(
            name='Salary',
            label=KakeiboLabel.INCOME,
            user=self.user
        )
        self.assertEqual(str(category), 'Salary')
        self.assertEqual(category.label, KakeiboLabel.INCOME)
        self.assertEqual(category.user, self.user)

    def test_create_income(self):
        """Test creating an income record."""
        category = Categories.objects.create(name='Salary', label=KakeiboLabel.INCOME, user=self.user)
        income = Incomes.objects.create(
            amount=300000,
            category=category,
            user=self.user
        )
        self.assertEqual(str(income), '300000')
        self.assertEqual(income.category.name, 'Salary')

    def test_create_expenditure(self):
        """Test creating an expenditure record."""
        category = Categories.objects.create(name='Groceries', label=KakeiboLabel.EXPENDITURE, user=self.user)
        expenditure = Expenditures.objects.create(
            amount=5000,
            category=category,
            user=self.user
        )
        self.assertEqual(str(expenditure), '5000')
        self.assertEqual(expenditure.category.name, 'Groceries')

    def test_income_category_protection(self):
        """Test that a category linked to an income cannot be deleted."""
        category = Categories.objects.create(name='Part-time Job', label=KakeiboLabel.INCOME, user=self.user)
        Incomes.objects.create(amount=50000, category=category, user=self.user)
        
        with self.assertRaises(ProtectedError):
            category.delete()

    def test_expenditure_category_protection(self):
        """Test that a category linked to an expenditure cannot be deleted."""
        category = Categories.objects.create(name='Utilities', label=KakeiboLabel.EXPENDITURE, user=self.user)
        Expenditures.objects.create(amount=10000, category=category, user=self.user)

        with self.assertRaises(ProtectedError):
            category.delete()