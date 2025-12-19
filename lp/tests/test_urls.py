from django.test import TestCase
from django.urls import reverse, resolve
from lp.views import General


class LpUrlsTests(TestCase):
    def test_general_url_resolves(self):
        """Test that the 'general' url resolves to the General view."""
        url = reverse('lp:general')
        self.assertEqual(resolve(url).func.view_class, General)