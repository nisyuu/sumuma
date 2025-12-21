from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from kakeibo.models import Categories, Incomes, Expenditures, KakeiboLabel
import datetime

User = get_user_model()


class AnalysesViewsTests(TestCase):

    def setUp(self):
        """Set up data for analysis view tests."""
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client = Client()
        self.client.login(email='testuser@example.com', password='testpassword')

        # Create some data for the user to analyze
        today = datetime.date.today()
        one_month_ago = today - datetime.timedelta(days=30)

        self.income_cat = Categories.objects.create(user=self.user, name='Salary', label=KakeiboLabel.INCOME)
        self.exp_cat1 = Categories.objects.create(user=self.user, name='Food', label=KakeiboLabel.EXPENDITURE)
        self.exp_cat2 = Categories.objects.create(user=self.user, name='Transport', label=KakeiboLabel.EXPENDITURE)

        Incomes.objects.create(user=self.user, category=self.income_cat, amount=300000, event_date=today)
        Expenditures.objects.create(user=self.user, category=self.exp_cat1, amount=2000, event_date=today)
        Expenditures.objects.create(user=self.user, category=self.exp_cat2, amount=500, event_date=today)
        Expenditures.objects.create(user=self.user, category=self.exp_cat1, amount=1500, event_date=one_month_ago)

    def test_top_view(self):
        """Test the Top analysis view."""
        response = self.client.get(reverse('analyses:top'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyses/top.html')
        self.assertIn('expenditure_or_income_records', response.context)
        self.assertIn('total_expenditures', response.context)

    def test_transition_view(self):
        """Test the Transition analysis view."""
        response = self.client.get(reverse('analyses:transition'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyses/transition.html')
        self.assertIn('event_date', response.context)
        self.assertIn('total_amount', response.context)

    def test_accumulation_view(self):
        """Test the Accumulation analysis view."""
        response = self.client.get(reverse('analyses:accumulation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyses/accumulation.html')
        self.assertIn('event_date', response.context)
        self.assertIn('expenditure_or_income_records', response.context)

    def test_analyses_by_category_view(self):
        """Test the AnalysesByCategory view."""
        response = self.client.get(reverse('analyses:analyses_by_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyses/analyses_by_category.html')
        self.assertIn('categories', response.context)

    def test_search_pie_each_month_view(self):
        """Test the search_pie_each_month function view."""
        # Test with valid parameters for a previous month
        one_month_ago = datetime.date.today() - datetime.timedelta(days=30)
        url = f"{reverse('analyses:search_pie_each_month')}?year_and_month={one_month_ago.strftime('%Y-%m')}&expenditure_or_income=expenditure"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyses/top.html')
        self.assertIn('total_expenditures', response.context)

    def test_search_pie_each_month_invalid_redirects(self):
        """Test that the search view redirects if parameters are invalid or for the current month."""
        # Test for current month, which should redirect
        today = datetime.date.today()
        url = f"{reverse('analyses:search_pie_each_month')}?year_and_month={today.strftime('%Y-%m')}&expenditure_or_income=expenditure"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('analyses:top'))
        
        # Test with invalid parameters
        url = f"{reverse('analyses:search_pie_each_month')}?year_and_month=bad-date&expenditure_or_income=expenditure"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Should redirect because _validate_search fails