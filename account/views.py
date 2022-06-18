from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import generic
from sumuma.concerns.permission import OnlyYouMixin

from .forms import (
    LoginForm, SignupForm, UpdateUserForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)

User = get_user_model()


class Login(LoginView):
    """Login view."""
    template_name = 'account/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('kakeibo:top')
        return super(Login, self).dispatch(request, *args, **kwargs)


class Logout(LoginRequiredMixin, LogoutView):
    """Logout view."""
    template_name = 'home/top.html'


class Signup(generic.CreateView):
    """Signup view."""
    template_name = 'account/signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # NOTE: Send activation email
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('account/mail_template/activation/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('account/mail_template/activation/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('account:complete_provisional_registration')


class CompleteProvisionalRegistration(generic.TemplateView):
    """
    Complete sending provisional registration email view.
    """
    template_name = 'account/complete_provisional_registration.html'


class Activated(generic.TemplateView):
    """Activation view."""
    template_name = 'account/activated.html'
    # NOTE: activation url is expired over 24 hour after sending activation email.
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS')

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # NOTE: expired
        except SignatureExpired:
            return HttpResponseBadRequest()

        # NOTE: mistake token
        except BadSignature:
            return HttpResponseBadRequest()

        # NOTE: no problem
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoenNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class PasswordReset(PasswordResetView):
    """Password reset for who forgot password."""
    subject_template_name = 'account/mail_template/password_reset/subject.txt'
    email_template_name = 'account/mail_template/password_reset/message.txt'
    template_name = 'account/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('account:accept_password_reset')


class AcceptPasswordReset(PasswordResetDoneView):
    """Accept password reset view."""
    template_name = 'account/accept_password_reset.html'


class SetPassword(PasswordResetConfirmView):
    """Set password for people who forgot password."""
    form_class = SetPasswordForm
    success_url = reverse_lazy('account:complete_password_reset')
    template_name = 'account/set_password.html'


class CompletePasswordReset(PasswordResetCompleteView):
    """Complete password reset view who forgot password."""
    template_name = 'account/complete_provisional_registration.html'


# NOTE: internal views of dashboard


class UserDetail(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    """User detail view."""
    model = User
    template_name = 'account/user_detail.html'


class UpdateUser(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    """Update user view."""
    model = User
    form_class = UpdateUserForm
    template_name = 'account/update_user.html'

    def get_success_url(self):
        messages.success(self.request, 'ユーザー情報を変更しました。')
        return resolve_url('account:user_detail', pk=self.kwargs['pk'])


class PasswordChange(LoginRequiredMixin, OnlyYouMixin, PasswordChangeView):
    """Password change view."""
    form_class = PasswordChangeForm
    template_name = 'account/password_change.html'

    def get_success_url(self):
        messages.success(self.request, 'パスワードを変更しました。')
        return resolve_url('account:user_detail', pk=self.kwargs['pk'])
