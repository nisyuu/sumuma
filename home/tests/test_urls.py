from django.test import TestCase
from django.urls import reverse, resolve
from home.views import Top, TermsOfService, PrivacyPolicy


class HomeUrlsTests(TestCase):
    def test_top_url_resolves(self):
        """Test that the 'top' url resolves to the Top view."""
        url = reverse('home:top')
        self.assertEqual(resolve(url).func.view_class, Top)

    def test_terms_of_service_url_resolves(self):
        """Test that the 'terms_of_service' url resolves to the TermsOfService view."""
        url = reverse('home:terms_of_service')
        self.assertEqual(resolve(url).func.view_class, TermsOfService)

    def test_privacy_policy_url_resolves(self):
        """Test that the 'privacy_policy' url resolves to the PrivacyPolicy view."""
        url = reverse('home:privacy_policy')
        self.assertEqual(resolve(url).func.view_class, PrivacyPolicy)