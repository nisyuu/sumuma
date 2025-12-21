from django.test import TestCase
from django.urls import reverse, resolve
from kakeibo.views import kakeibo, records


class KakeiboUrlsTests(TestCase):
    def test_top_url_resolves(self):
        """Test 'top' url resolves to the correct view."""
        url = reverse('kakeibo:top')
        self.assertEqual(resolve(url).func.view_class, kakeibo.Top)

    def test_create_income_url_resolves(self):
        """Test 'create_income' url resolves to the correct view."""
        url = reverse('kakeibo:create_income')
        self.assertEqual(resolve(url).func.view_class, kakeibo.CreateIncome)

    def test_edit_income_url_resolves(self):
        """Test 'edit_income' url with a pk resolves to the correct view."""
        url = reverse('kakeibo:edit_income', args=[1])
        self.assertEqual(resolve(url).func.view_class, kakeibo.EditIncome)

    def test_delete_income_url_resolves(self):
        """Test 'delete_income' url with a pk resolves to the correct view."""
        url = reverse('kakeibo:delete_income', args=[1])
        self.assertEqual(resolve(url).func, kakeibo.delete_income)

    def test_records_top_url_resolves(self):
        """Test 'records_top' url resolves to the correct view."""
        url = reverse('kakeibo:records_top')
        self.assertEqual(resolve(url).func.view_class, records.Top)

    def test_records_edit_expenditure_url_resolves(self):
        """Test 'records_edit_expenditure' url with a pk resolves to the correct view."""
        url = reverse('kakeibo:records_edit_expenditure', args=[1])
        self.assertEqual(resolve(url).func.view_class, records.EditExpenditure)
    
    def test_records_export_url_resolves(self):
        """Test 'records_export' url resolves to the correct view."""
        url = reverse('kakeibo:records_export')
        self.assertEqual(resolve(url).func, records.records_export)