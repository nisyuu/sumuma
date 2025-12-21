from django.test import TestCase
from django.core import mail
from contact.forms import ContactForm


class ContactFormsTests(TestCase):
    def test_contact_form_valid(self):
        """Test the ContactForm with valid data."""
        form_data = {
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data=form_data, email='test@example.com')
        self.assertTrue(form.is_valid())

    def test_contact_form_missing_subject(self):
        """Test the form is invalid if subject is missing."""
        form_data = {'message': 'This is a test message.'}
        form = ContactForm(data=form_data, email='test@example.com')
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)

    def test_contact_form_send_email(self):
        """Test the form's send_email method."""
        form_data = {
            'subject': 'Inquiry about your service',
            'message': 'Hello, I would like to know more.'
        }
        form = ContactForm(data=form_data, email='customer@example.com')
        self.assertTrue(form.is_valid())
        
        form.send_email()

        # Check that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        
        # Verify the contents of the email.
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Inquiry about your service')
        self.assertEqual(email.body, 'Hello, I would like to know more.')
        self.assertEqual(email.from_email, 'customer@example.com')
        self.assertEqual(email.to, ['info@sumuma.com'])