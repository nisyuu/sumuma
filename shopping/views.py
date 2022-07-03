from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateToDoForm
from .models import ToDo

User = get_user_model()


class Top(LoginRequiredMixin, generic.ListView):
    template_name = 'shopping/todo.html'
    context_object_name = 'todos'
    paginate_by = 50
    model = ToDo


class CreateToDo(LoginRequiredMixin, generic.CreateView):
    model = ToDo
    form_class = CreateToDoForm
    template_name = 'shopping/create.html'
    success_url = reverse_lazy('shopping:top')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, '登録しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '登録に失敗しました。')
        return redirect(self.success_url)
