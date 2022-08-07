from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from kakeibo.models import Expenditures
from sumuma.concerns.permission import OnlyYouToDoMixin
from .forms import ToDoForm
from .models import ToDo

User = get_user_model()


class Top(LoginRequiredMixin, generic.ListView):
    template_name = 'shopping/todo.html'
    context_object_name = 'todos'
    paginate_by = 100
    model = ToDo

    def get_queryset(self):
        if self.request.GET.get('is_all') == 'on':
            return ToDo.objects.filter(user=self.request.user)
        return ToDo.objects.filter(is_bought=False, user=self.request.user)


class CreateToDo(LoginRequiredMixin, generic.CreateView):
    model = ToDo
    form_class = ToDoForm
    template_name = 'shopping/create_todo.html'
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


class EditToDo(LoginRequiredMixin, OnlyYouToDoMixin, generic.UpdateView):
    model = ToDo
    form_class = ToDoForm
    template_name = 'shopping/edit_todo.html'
    success_url = reverse_lazy('shopping:top')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    @transaction.atomic
    def form_valid(self, form):
        user = self.request.user
        instance = form.instance
        form.instance.user = user
        if instance.is_registered and not form.instance.expenditure:
            expenditure = Expenditures.objects.create(user=user, category=instance.category,
                                                      event_date=instance.event_date,
                                                      amount=instance.amount, memo=instance.memo)
            form.instance.expenditure = expenditure
        form.save()
        messages.success(self.request, '更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '更新に失敗しました。')
        return redirect(self.success_url)


class DeleteToDo(LoginRequiredMixin, OnlyYouToDoMixin, generic.DeleteView):
    model = ToDo
    success_url = reverse_lazy('shopping:top')

    def form_valid(self, form):
        ToDo.objects.get(id=self.kwargs['pk']).delete()
        messages.success(self.request, '削除しました。')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.success(self.request, '削除に失敗しました。')
        return redirect(self.success_url)
