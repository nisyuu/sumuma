from django.test import TestCase, Client
from django.urls import reverse


class LpViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_general_view(self):
        """Test the General view returns a 200 status code and uses the correct template."""
        url = reverse('lp:general')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lp/general.html')