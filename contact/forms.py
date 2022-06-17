from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    subject = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={
                                  'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border '
                                           'border-gray-200 rounded py-3 px-4 '
                                           'leading-tight focus:outline-none focus:bg-white focus:border-gray-300'})
                              )
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={
                                  'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border '
                                           'border-gray-200 rounded py-3 px-4 '
                                           'leading-tight focus:outline-none focus:bg-white focus:border-gray-300'})
                              )

    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop('email')
        super(ContactForm, self).__init__(*args, **kwargs)

    def send_email(self):
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        from_email = self.email
        to = ['info@daihuku.xyz']

        send_mail(subject, message, from_email, to)
