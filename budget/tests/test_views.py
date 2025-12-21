from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from kakeibo.models import Categories, Expenditures, KakeiboLabel
from budget.models import ExpenditurePlans
import datetime
from dateutil.relativedelta import relativedelta

User = get_user_model()


class BudgetViewsTests(TestCase):

    def setUp(self):
        """Set up data for budget view tests."""
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client = Client()
        self.client.login(email='testuser@example.com', password='testpassword')

        self.cat1 = Categories.objects.create(user=self.user, name='Food', label=KakeiboLabel.EXPENDITURE)
        self.cat2 = Categories.objects.create(user=self.user, name='Transport', label=KakeiboLabel.EXPENDITURE)

        self.today = datetime.date.today()
        self.bom = self.today.replace(day=1) # Beginning of Month

        # Create plans for the current month
        self.plan1 = ExpenditurePlans.objects.create(user=self.user, category=self.cat1, event_date=self.bom, amount=30000)
        
        # Create actual expenditures for the current month
        Expenditures.objects.create(user=self.user, category=self.cat1, amount=1500, event_date=self.today)

    def test_top_view(self):
        """Test the Top budget view."""
        response = self.client.get(reverse('budget:top'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/top.html')
        self.assertIn('expenditure_condition', response.context)
        self.assertIn('sum_budget', response.context)
        # Check that the calculated sum_budget is correct
        self.assertEqual(response.context['sum_budget'], 30000)
        self.assertEqual(sum(response.context['expenditure_records']), 1500)

    def test_create_view(self):
        """Test the Create budget view."""
        url = f"{reverse('budget:create')}?year_and_month={self.today.strftime('%Y-%m')}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/create.html')
        self.assertIn('form', response.context)
        self.assertIn('categories', response.context)

    def test_expenditure_plan_save_view(self):
        """Test the expenditure_plan_save function view."""
        # First, delete the existing plan to avoid the "already exists" error
        self.plan1.delete()
        
        url = reverse('budget:expenditure_plan_save')
        data = {
            'year_and_month': self.bom.strftime('%Y-%m-%d'),
            'category_ids': [self.cat1.pk, self.cat2.pk],
            'amount': [50000, 10000],
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('budget:top'))
        
        # Check that two plans were created
        self.assertEqual(ExpenditurePlans.objects.filter(user=self.user, event_date=self.bom).count(), 2)
        new_plan1 = ExpenditurePlans.objects.get(user=self.user, category=self.cat1, event_date=self.bom)
        self.assertEqual(new_plan1.amount, 50000)

    def test_copy_last_month_expenditure_plans(self):
        """Test the copy_last_month_expenditure_plans view."""
        # Create a plan for last month
        last_month_date = self.bom - relativedelta(months=1)
        ExpenditurePlans.objects.create(user=self.user, category=self.cat1, event_date=last_month_date, amount=25000)
        
        # Delete the plan for the current month so we can copy into it
        self.plan1.delete()

        url = reverse('budget:copy_last_month_expenditure_plans')
        data = {'year_and_month': self.bom.strftime('%Y-%m')}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('budget:top'))

        # Check that the plan for the current month was created by copying
        self.assertTrue(ExpenditurePlans.objects.filter(user=self.user, event_date=self.bom.strftime('%Y-%m-01')).exists())
        copied_plan = ExpenditurePlans.objects.get(user=self.user, event_date=self.bom.strftime('%Y-%m-01'), category=self.cat1)
        self.assertEqual(copied_plan.amount, 25000)