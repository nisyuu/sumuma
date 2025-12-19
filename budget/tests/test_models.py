from django.test import TestCase
from django.contrib.auth import get_user_model
from kakeibo.models import Categories, KakeiboLabel
from budget.models import ExpenditurePlans
import datetime

User = get_user_model()


class BudgetModelTests(TestCase):
    def setUp(self):
        """Create a user and a category for tests."""
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.category = Categories.objects.create(
            user=self.user,
            name='Groceries',
            label=KakeiboLabel.EXPENDITURE
        )

    def test_create_expenditure_plan(self):
        """Test creating an ExpenditurePlans object."""
        plan = ExpenditurePlans.objects.create(
            user=self.user,
            category=self.category,
            event_date=datetime.date.today(),
            amount=50000
        )
        self.assertEqual(plan.user, self.user)
        self.assertEqual(plan.category, self.category)
        self.assertEqual(plan.amount, 50000)
        self.assertEqual(str(plan), '50000')