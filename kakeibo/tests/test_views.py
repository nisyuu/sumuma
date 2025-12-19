from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from kakeibo.models import Categories, Incomes, Expenditures, KakeiboLabel
import datetime

User = get_user_model()


class KakeiboViewsTests(TestCase):

    def setUp(self):
        """Set up data for view tests."""
        # Create users
        self.user1 = User.objects.create_user(email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password')

        # Create clients and log them in
        self.client1 = Client()
        self.client1.login(email='user1@example.com', password='password')

        # Data for user1
        self.user1_income_cat = Categories.objects.create(user=self.user1, name='Salary', label=KakeiboLabel.INCOME)
        self.user1_exp_cat = Categories.objects.create(user=self.user1, name='Food', label=KakeiboLabel.EXPENDITURE)
        self.user1_income = Incomes.objects.create(user=self.user1, category=self.user1_income_cat, amount=1000)
        self.user1_exp = Expenditures.objects.create(user=self.user1, category=self.user1_exp_cat, amount=100)

        # Data for user2
        self.user2_income_cat = Categories.objects.create(user=self.user2, name='Bonus', label=KakeiboLabel.INCOME)
        self.user2_income = Incomes.objects.create(user=self.user2, category=self.user2_income_cat, amount=500)

    def test_top_view_authenticated(self):
        """Test that the top view is accessible for a logged-in user."""
        response = self.client1.get(reverse('kakeibo:top'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kakeibo/top.html')
        # Check that only user1's records are in the queryset
        self.assertIn(self.user1_income, response.context['records'])
        self.assertNotIn(self.user2_income, response.context['records'])

    def test_top_view_unauthenticated(self):
        """Test that an unauthenticated user is redirected to the login page."""
        unauthenticated_client = Client()
        response = unauthenticated_client.get(reverse('kakeibo:top'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account:login')}?next={reverse('kakeibo:top')}")

    def test_create_income_valid(self):
        """Test creating an income with a valid POST request."""
        url = reverse('kakeibo:create_income')
        data = {
            'amount': 2000,
            'category': self.user1_income_cat.pk,
            'event_date': datetime.date.today()
        }
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('kakeibo:top'))
        self.assertTrue(Incomes.objects.filter(user=self.user1, amount=2000).exists())
        
        # Test that a success message was sent
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '収入を登録しました。')

    def test_edit_income_permission(self):
        """Test that a user cannot edit another user's income."""
        url = reverse('kakeibo:edit_income', args=[self.user2_income.pk])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, 404) # OnlyYou mixin should cause a 404

    def test_delete_income(self):
        """Test that a user can delete their own income."""
        url = reverse('kakeibo:delete_income', args=[self.user1_income.pk])
        response = self.client1.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('kakeibo:top'))
        
        # Verify the object is soft-deleted
        self.user1_income.refresh_from_db()
        self.assertTrue(self.user1_income.deleted)