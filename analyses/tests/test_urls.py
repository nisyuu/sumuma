from django.test import TestCase
from django.urls import reverse, resolve
from analyses.views import (
    Top, Accumulation, Transition, AnalysesByCategory, search_pie_each_month
)


class AnalysesUrlsTests(TestCase):
    def test_top_url_resolves(self):
        """Test 'top' url resolves to the correct view."""
        url = reverse('analyses:top')
        self.assertEqual(resolve(url).func.view_class, Top)

    def test_accumulation_url_resolves(self):
        """Test 'accumulation' url resolves to the correct view."""
        url = reverse('analyses:accumulation')
        self.assertEqual(resolve(url).func.view_class, Accumulation)

    def test_transition_url_resolves(self):
        """Test 'transition' url resolves to the correct view."""
        url = reverse('analyses:transition')
        self.assertEqual(resolve(url).func.view_class, Transition)

    def test_analyses_by_category_url_resolves(self):
        """Test 'analyses_by_category' url resolves to the correct view."""
        url = reverse('analyses:analyses_by_category')
        self.assertEqual(resolve(url).func.view_class, AnalysesByCategory)
        
    def test_search_pie_each_month_url_resolves(self):
        """Test 'search_pie_each_month' url resolves to the correct view."""
        url = reverse('analyses:search_pie_each_month')
        self.assertEqual(resolve(url).func, search_pie_each_month)