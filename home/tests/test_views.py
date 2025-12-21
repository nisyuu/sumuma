from django.test import TestCase, Client
from django.urls import reverse


class HomeViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_top_view(self):
        """Test the Top view returns a 200 status code and uses the correct template."""
        url = reverse('home:top')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/top.html')

    def test_terms_of_service_view(self):
        """Test the TermsOfService view redirects correctly."""
        url = reverse('home:terms_of_service')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, 'https://alwaysblue.notion.site/4117c20f7d4149fb90dde04989be0299')

    def test_privacy_policy_view(self):
        """Test the PrivacyPolicy view redirects correctly."""
        url = reverse('home:privacy_policy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, 'https://alwaysblue.notion.site/842a8798e57d4bc3ac0961ed1d664ff7')