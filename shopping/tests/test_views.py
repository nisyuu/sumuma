from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from kakeibo.models import Categories, Expenditures, KakeiboLabel
from shopping.models import ToDo
import datetime

User = get_user_model()


class ShoppingViewsTests(TestCase):

    def setUp(self):
        """Set up data for view tests."""
        self.user1 = User.objects.create_user(email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password')

        self.client1 = Client()
        self.client1.login(email='user1@example.com', password='password')

        self.user1_cat = Categories.objects.create(user=self.user1, name='Groceries', label=KakeiboLabel.EXPENDITURE)

        # ToDo items for user1
        self.todo1_user1 = ToDo.objects.create(user=self.user1, name='Buy Milk', is_bought=False)
        self.todo2_user1_bought = ToDo.objects.create(user=self.user1, name='Buy Bread', is_bought=True)

        # ToDo item for user2
        self.todo1_user2 = ToDo.objects.create(user=self.user2, name='Buy Juice', is_bought=False)

    def test_top_view_shows_own_unbought_todos(self):
        """Test the top view shows only the logged-in user's unbought ToDo items."""
        response = self.client1.get(reverse('shopping:top'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping/todo.html')
        self.assertIn(self.todo1_user1, response.context['todos'])
        self.assertNotIn(self.todo2_user1_bought, response.context['todos'])
        self.assertNotIn(self.todo1_user2, response.context['todos'])

    def test_top_view_is_all_filter(self):
        """Test the 'is_all=on' filter shows all of the user's ToDo items."""
        response = self.client1.get(reverse('shopping:top') + '?is_all=on')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.todo1_user1, response.context['todos'])
        self.assertIn(self.todo2_user1_bought, response.context['todos'])
        self.assertNotIn(self.todo1_user2, response.context['todos'])
        
    def test_create_todo_view(self):
        """Test creating a ToDo item via the view."""
        url = reverse('shopping:create_todo')
        data = {'name': 'Buy Cheese'}
        response = self.client1.post(url, data)
        self.assertRedirects(response, reverse('shopping:top'))
        self.assertTrue(ToDo.objects.filter(user=self.user1, name='Buy Cheese').exists())

    def test_edit_todo_permission_denied(self):
        """Test a user cannot access the edit page for another user's ToDo."""
        url = reverse('shopping:edit_todo', args=[self.todo1_user2.pk])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, 403) # OnlyYouToDoMixin should raise 403

    def test_edit_todo_creates_expenditure(self):
        """Test that editing a ToDo with 'is_registered' creates an Expenditure."""
        self.assertEqual(Expenditures.objects.count(), 0)
        
        url = reverse('shopping:edit_todo', args=[self.todo1_user1.pk])
        data = {
            'name': 'Buy Milk and Cheese',
            'amount': 1200,
            'category': self.user1_cat.pk,
            'event_date': datetime.date.today(),
            'is_bought': 'on',
            'is_registered': 'on', # This should trigger expenditure creation
        }
        response = self.client1.post(url, data)
        self.assertRedirects(response, reverse('shopping:top'))

        # Check that one Expenditure was created
        self.assertEqual(Expenditures.objects.count(), 1)
        expenditure = Expenditures.objects.first()
        self.assertEqual(expenditure.amount, 1200)
        self.assertEqual(expenditure.user, self.user1)

        # Check that the ToDo was updated and linked to the expenditure
        self.todo1_user1.refresh_from_db()
        self.assertEqual(self.todo1_user1.name, 'Buy Milk and Cheese')
        self.assertTrue(self.todo1_user1.is_bought)
        self.assertTrue(self.todo1_user1.is_registered)
        self.assertEqual(self.todo1_user1.expenditure, expenditure)
        
    def test_delete_todo_view(self):
        """Test that a user can delete their own ToDo item."""
        todo_count_before = ToDo.objects.filter(user=self.user1).count()
        url = reverse('shopping:delete_todo', args=[self.todo1_user1.pk])
        response = self.client1.post(url)
        self.assertRedirects(response, reverse('shopping:top'))
        self.assertEqual(ToDo.objects.filter(user=self.user1).count(), todo_count_before - 1)