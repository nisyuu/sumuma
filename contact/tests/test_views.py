from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()


class ContactViewsTests(TestCase):

    def setUp(self):
        """Set up user and client for view tests."""
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client = Client()
        self.client.login(email='testuser@example.com', password='testpassword')
        self.url = reverse('contact:top')

    def test_contact_view_get(self):
        """Test GET request to the contact view."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/top.html')
        self.assertIn('form', response.context)

    def test_contact_view_unauthenticated(self):
        """Test that an unauthenticated user is redirected."""
        unauthenticated_client = Client()
        response = unauthenticated_client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account:login').rstrip('/'), response.url)

    def test_contact_view_post_valid(self):
        """Test a valid POST request sends an email and redirects."""
        form_data = {
            'subject': 'Hello from the test suite',
            'message': 'This is a test submission.'
        }
        response = self.client.post(self.url, form_data, follow=True)
        
        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Hello from the test suite')
        self.assertEqual(email.from_email, self.user.email)

        # Check for redirect and success message on the final page
        self.assertRedirects(response, self.url, status_code=302, target_status_code=200)
        self.assertContains(response, 'メッセージを送信しました。')

    def test_contact_view_post_invalid(self):
        """Test an invalid POST request does not send an email and shows an error."""
        form_data = {'subject': 'Only a subject'} # Missing message
        response = self.client.post(self.url, form_data, follow=True)
        
        # Check that no email was sent
        self.assertEqual(len(mail.outbox), 0)

        # Check for redirect and error message
        self.assertRedirects(response, self.url, status_code=302, target_status_code=200)
        self.assertContains(response, 'メッセージの送信に失敗しました。')