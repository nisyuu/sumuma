from django.test import TestCase
from django.contrib.auth import get_user_model
from kakeibo.models import Categories, KakeiboLabel
from shopping.models import ToDo

User = get_user_model()


class ShoppingModelTests(TestCase):
    def setUp(self):
        """Create a user and a category for all tests in this class."""
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.category = Categories.objects.create(
            user=self.user,
            name='Groceries',
            label=KakeiboLabel.EXPENDITURE
        )

    def test_create_todo_minimal(self):
        """Test creating a ToDo item with minimal data."""
        todo = ToDo.objects.create(
            name='Buy milk',
            user=self.user
        )
        self.assertEqual(todo.name, 'Buy milk')
        self.assertEqual(todo.user, self.user)
        self.assertFalse(todo.is_bought)

    def test_create_todo_full(self):
        """Test creating a ToDo item with all data."""
        todo = ToDo.objects.create(
            name='Buy apples',
            amount=500,
            category=self.category,
            user=self.user,
            memo='Red apples'
        )
        self.assertEqual(todo.name, 'Buy apples')
        self.assertEqual(todo.amount, 500)
        self.assertEqual(str(todo), '500') # __str__ returns the amount
        self.assertEqual(todo.category, self.category)
        self.assertEqual(todo.user, self.user)