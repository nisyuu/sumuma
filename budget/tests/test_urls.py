from django.test import TestCase
from django.urls import reverse, resolve
from budget.views import (
    Top, Create, Edit, expenditure_plan_save, expenditure_plan_update, copy_last_month_expenditure_plans
)


class BudgetUrlsTests(TestCase):
    def test_top_url_resolves(self):
        """Test 'top' url resolves to the correct view."""
        url = reverse('budget:top')
        self.assertEqual(resolve(url).func.view_class, Top)

    def test_create_url_resolves(self):
        """Test 'create' url resolves to the correct view."""
        url = reverse('budget:create')
        self.assertEqual(resolve(url).func.view_class, Create)

    def test_edit_url_resolves(self):
        """Test 'edit' url resolves to the correct view."""
        url = reverse('budget:edit')
        self.assertEqual(resolve(url).func.view_class, Edit)

    def test_expenditure_plan_save_url_resolves(self):
        """Test 'expenditure_plan_save' url resolves to the correct view."""
        url = reverse('budget:expenditure_plan_save')
        self.assertEqual(resolve(url).func, expenditure_plan_save)

    def test_expenditure_plan_update_url_resolves(self):
        """Test 'expenditure_plan_update' url resolves to the correct view."""
        url = reverse('budget:expenditure_plan_update')
        self.assertEqual(resolve(url).func, expenditure_plan_update)

    def test_copy_last_month_url_resolves(self):
        """Test 'copy_last_month_expenditure_plans' url resolves to the correct view."""
        url = reverse('budget:copy_last_month_expenditure_plans')
        self.assertEqual(resolve(url).func, copy_last_month_expenditure_plans)