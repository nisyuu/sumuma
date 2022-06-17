from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ContactForm


class Top(LoginRequiredMixin, FormView):
    template_name = 'contact/top.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:top')

    def get_form_kwargs(self):
        kwargs = super(Top, self).get_form_kwargs()
        kwargs['email'] = self.request.user.email
        return kwargs

    def form_valid(self, form):

        try:
            form.send_email()
        except BadHeaderError:
            messages.error(self.request, 'メッセージの送信に失敗しました。')
            return redirect('contact:top')

        messages.success(self.request, 'メッセージを送信しました。')
        return super(Top, self).form_valid(form)

    def form_invalid(self, form):

        messages.error(self.request, 'メッセージの送信に失敗しました。')
        return redirect('contact:top')
