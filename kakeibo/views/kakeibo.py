import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from itertools import chain

from kakeibo.forms import ExpenditureForm, IncomeForm, CategoryForm
from kakeibo.models import Expenditures, Incomes, Categories
from sumuma.concerns.permission import OnlyYouExpenditureMixin, OnlyYouIncomeMixin

User = get_user_model()


class Top(LoginRequiredMixin, generic.ListView):
    template_name = 'kakeibo/top.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        today = datetime.today()
        one_month_ago_date = today - relativedelta(months=1, days=1)
        incomes_record = Incomes.objects.filter(user_id=self.request.user.id,
                                                event_date__range=[one_month_ago_date, today],
                                                deleted=False).select_related('category')
        expenditures_record = Expenditures.objects.filter(user_id=self.request.user.id,
                                                     event_date__range=[one_month_ago_date, today],
                                                     deleted=False).select_related('category')
        return sorted(chain(incomes_record, expenditures_record), key=lambda instance: instance.event_date, reverse=True)

    def get_context_data(self, **kwargs):
        one_month_ago_date = datetime.today() - relativedelta(months=1, days=1)
        context = super().get_context_data(**kwargs)
        event_date = []
        incomes = []
        expenditures = []
        for day in range(32):
            date = one_month_ago_date + timedelta(day)
            income = \
                Incomes.objects.filter(user_id=self.request.user.id, event_date=date, deleted=False).aggregate(
                    sum_amount=Sum('amount'))['sum_amount']
            expenditure = \
                Expenditures.objects.filter(user_id=self.request.user.id, event_date=date, deleted=False).aggregate(
                    sum_amount=Sum('amount'))['sum_amount']
            if income:
                incomes.append(income)
            else:
                incomes.append(0)
            if expenditure:
                expenditures.append(expenditure)
            else:
                expenditures.append(0)
            event_date.append('{}/{}'.format(date.month, date.day))
        context['submit_token'] = set_submit_token(self.request)
        context['event_date'] = event_date
        context['incomes'] = incomes
        context['expenditures'] = expenditures
        context['expenditure_categories'] = Categories.objects.filter(
            label='expenditure',
            user=self.request.user
        ).values_list('id', flat=True)
        context['income_categories'] = Categories.objects.filter(
            label='income',
            user=self.request.user
        ).values_list('id', flat=True)
        return context

    def income_form(self):
        return IncomeForm(user=self.request.user)

    def expenditure_form(self):
        return ExpenditureForm(user=self.request.user)


class CreateIncome(LoginRequiredMixin, generic.CreateView):
    model = Incomes
    form_class = IncomeForm
    template_name = 'kakeibo/top.html'
    success_url = reverse_lazy('kakeibo:top')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, '収入を登録しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '登録に失敗しました。')
        return redirect(self.success_url)
        return redirect(self.success_url)


class CreateExpenditure(LoginRequiredMixin, generic.CreateView):
    model = Expenditures
    form_class = ExpenditureForm
    template_name = 'kakeibo/top.html'
    success_url = reverse_lazy('kakeibo:top')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, '支出を登録しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '登録に失敗しました。')
        return redirect(self.success_url)


class EditExpenditure(LoginRequiredMixin, OnlyYouExpenditureMixin, generic.UpdateView, generic.FormView):
    template_name = 'kakeibo/edit.html'
    model = Expenditures
    form_class = ExpenditureForm
    success_url = reverse_lazy('kakeibo:top')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        messages.success(self.request, "編集を更新しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新できませんでした。")
        return redirect(self.success_url)


class EditIncome(LoginRequiredMixin, OnlyYouIncomeMixin, generic.UpdateView, generic.FormView):
    template_name = 'kakeibo/edit.html'
    model = Incomes
    form_class = IncomeForm
    success_url = reverse_lazy('kakeibo:top')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        messages.success(self.request, "編集を更新しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新できませんでした。")


def delete_income(request, pk):
    if request.method == 'POST':
        income = Incomes.objects.get(pk=pk)
        income.deleted = True
        income.save()
        messages.success(request, '削除しました。')
        return redirect('kakeibo:top')


def delete_expenditure(request, pk):
    if request.method == 'POST':
        expenditure = Expenditures.objects.get(pk=pk)
        expenditure.deleted = True
        expenditure.save()
        messages.success(request, '削除しました。')
        return redirect('kakeibo:top')


def exists_submit_token(request):
    token_in_request = request.POST.get('submit_token')
    token_in_session = request.session.pop('submit_token', None)

    if not token_in_request:
        return False
    if not token_in_session:
        return False

    return token_in_request == token_in_session


def set_submit_token(request):
    submit_token = str(uuid.uuid4())
    request.session['submit_token'] = submit_token
    return submit_token


# NOTE: Category views


class CategoryIndex(LoginRequiredMixin, generic.ListView):
    template_name = 'kakeibo/categories.html'
    context_object_name = 'categories'
    model = Categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_token'] = set_submit_token(self.request)
        return context

    def category_form(self):
        return CategoryForm()


class CreateCategory(LoginRequiredMixin, generic.CreateView):
    model = Categories
    form_class = CategoryForm
    template_name = 'kakeibo/categories.html'
    success_url = reverse_lazy('kakeibo:categories')

    def form_valid(self, form):
        if not exists_submit_token(self.request):
            messages.error(self.request, '登録に失敗しました。')
            return redirect(self.success_url)

        existed_category = Categories.objects.filter(
            name=self.request.POST.get('name'),
            label=self.request.POST.get('label')
        ).first()

        if existed_category:
            messages.error(self.request, self.request.POST.get('name') + 'はすでに登録されています。')
            return redirect(self.success_url)

        form.instance.user = self.request.user
        messages.success(self.request, self.request.POST.get('name') + 'を登録しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '登録に失敗しました。')
        return redirect(self.success_url)


class DeleteCategory(LoginRequiredMixin, generic.DeleteView):
    model = Categories
    success_url = reverse_lazy('kakeibo:categories')

    def form_valid(self, form):
        Categories.objects.get(id=self.kwargs['pk']).delete()
        messages.success(self.request, '削除しました。')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.success(self.request, '削除に失敗しました。')
        return redirect(self.success_url)
