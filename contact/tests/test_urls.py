from django.test import TestCase
from django.urls import reverse, resolve
from contact.views import Top


class ContactUrlsTests(TestCase):
    def test_top_url_resolves(self):
        """Test that the 'top' url resolves to the Top view."""
        url = reverse('contact:top')
        self.assertEqual(resolve(url).func.view_class, Top)