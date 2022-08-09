from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm as PasswordChangeBaseForm,
    PasswordResetForm as PasswordResetBaseForm, SetPasswordForm as SetPasswordBaseForm
)

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Login form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'appearance-none block w-full bg-gray-200 text-gray-700 border ' \
                                          'border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none ' \
                                          'focus:bg-white'


class SignupForm(UserCreationForm):
    """Signup form."""

    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)
        else:
            fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'appearance-none block w-full bg-gray-200 text-gray-700 border ' \
                                          'border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none ' \
                                          'focus:bg-white'


class UpdateUserForm(forms.ModelForm):
    """Update user form."""

    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email', 'first_name', 'last_name')
        else:
            fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'appearance-none block w-full bg-gray-200 text-gray-700 border ' \
                                                     'border-gray-200 rounded py-3 px-4 leading-tight '
        self.fields['email'].widget.attrs['readonly'] = 'readonly'
        self.fields['last_name'].widget.attrs['class'] = 'appearance-none block w-full bg-gray-200 text-gray-700 ' \
                                                         'border border-gray-200 rounded py-3 px-4 leading-tight ' \
                                                         'focus:outline-none focus:bg-white focus:border-gray-300 '
        self.fields['first_name'].widget.attrs['class'] = 'appearance-none block w-full bg-gray-200 text-gray-700 ' \
                                                          'border border-gray-200 rounded py-3 px-4 leading-tight ' \
                                                          'focus:outline-none focus:bg-white focus:border-gray-300 '


class PasswordChangeForm(PasswordChangeBaseForm):
    """Password change form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'appearance-none block w-full bg-gray-200 text-gray-700 border ' \
                                          'border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none ' \
                                          'focus:bg-white'


class PasswordResetForm(PasswordResetBaseForm):
    """Password reset form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'appearance-none block w-full bg-gray-200 text-gray-700 border ' \
                                          'border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none ' \
                                          'focus:bg-white'


class SetPasswordForm(SetPasswordBaseForm):
    """Set password form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'appearance-none block w-full bg-gray-200 text-gray-700 border ' \
                                          'border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none ' \
                                          'focus:bg-white'
