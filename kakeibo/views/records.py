import csv
import urllib
from datetime import date, datetime
from io import TextIOWrapper
from itertools import chain

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from kakeibo.forms import IncomeForm, ExpenditureForm
from kakeibo.models import Incomes, Expenditures, Categories
from sumuma.concerns.permission import OnlyYouIncomeMixin, OnlyYouExpenditureMixin


def _get_beginning_of_month(year_and_month):
    beginning_of_month = year_and_month.strftime('%Y-%m-01')
    return datetime.strptime(beginning_of_month, '%Y-%m-%d')


def _get_end_of_month(year_and_month):
    beginning_of_month = year_and_month.strftime('%Y-%m-01')
    beginning_of_month = datetime.strptime(beginning_of_month, '%Y-%m-%d')
    end_of_month = beginning_of_month + relativedelta(months=1, days=-1)
    return end_of_month


class Top(LoginRequiredMixin, generic.ListView):
    template_name = 'records/top.html'
    context_object_name = 'records'
    paginate_by = 100

    def get_queryset(self):
        query = self.request.GET
        if query:
            category_ids = query.getlist('category_ids')
            start_date = query.get('start_date')
            end_date = query.get('end_date')
        else:
            today = date.today()
            category_ids = Categories.objects.filter(user=self.request.user).values_list('id', flat=True)
            start_date = _get_beginning_of_month(today)
            end_date = _get_end_of_month(today)

        if category_ids:
            income_records = Incomes.objects.filter(user_id=self.request.user.id,
                                                    category_id__in=category_ids,
                                                    event_date__range=[start_date, end_date],
                                                    deleted=False).select_related('category')
            expenditure_records = Expenditures.objects.filter(user_id=self.request.user.id,
                                                              category_id__in=category_ids,
                                                              event_date__range=[start_date, end_date],
                                                              deleted=False).select_related('category')
        else:
            income_records = Incomes.objects.filter(user_id=self.request.user.id,
                                                    event_date__range=[start_date, end_date],
                                                    deleted=False).select_related('category')
            expenditure_records = Expenditures.objects.filter(user_id=self.request.user.id,
                                                              event_date__range=[start_date, end_date],
                                                              deleted=False).select_related('category')
        return sorted(chain(income_records, expenditure_records), key=lambda instance: instance.event_date,
                      reverse=True)

    def get_context_data(self, **kwargs):
        context = super(Top, self).get_context_data(**kwargs)
        category_ids = Categories.objects.filter(user_id=self.request.user.id).values_list('id', flat=True)
        context['categories'] = Categories.objects.filter(id__in=category_ids)
        context['expenditure_categories'] = Categories.objects.filter(label='expenditure').values_list('id', flat=True)
        context['income_categories'] = Categories.objects.filter(label='income').values_list('id', flat=True)
        return context


def records_export(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    category_ids = request.POST.get('category_ids').split(',')
    today = date.today()
    if not start_date:
        start_date = _get_beginning_of_month(today)
    if not end_date:
        end_date = _get_end_of_month(today)
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    filename = urllib.parse.quote((datetime.today().strftime('%Y%m%dexport.csv')).encode('utf8'))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    if category_ids:
        income_record = Incomes.objects.filter(user_id=request.user.id, category_id__in=category_ids,
                                               event_date__range=[start_date, end_date],
                                               deleted=False).select_related('category')
        expenditure_record = Expenditures.objects.filter(user_id=request.user.id, category_id__in=category_ids,
                                                         event_date__range=[start_date, end_date],
                                                         deleted=False).select_related('category')
    else:
        income_record = Incomes.objects.filter(user_id=request.user.id, event_date__range=[start_date, end_date],
                                               deleted=False).select_related('category')
        expenditure_record = Expenditures.objects.filter(user_id=request.user.id,
                                                         event_date__range=[start_date, end_date],
                                                         deleted=False).select_related('category')
    records = sorted(chain(income_record, expenditure_record), key=lambda instance: instance.event_date, reverse=True)
    writer = csv.writer(response)
    writer.writerow(['', 'カテゴリ名', '日付', '金額', 'メモ'])
    for record in records:
        if record.category.label == 'expenditure':
            income_or_expenditure_label = '支出'
        else:
            income_or_expenditure_label = '収入'
        writer.writerow(
            [income_or_expenditure_label, record.category.name, record.event_date, record.amount, record.memo])
    return response


class EditExpenditure(LoginRequiredMixin, OnlyYouExpenditureMixin, generic.UpdateView):
    template_name = 'records/edit.html'
    model = Expenditures
    form_class = ExpenditureForm
    success_url = reverse_lazy('kakeibo:records_top')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existed_addition_category'] = list(
            Categories.objects.filter(user_id=self.request.user.id).values_list('id', flat=True))
        return context

    def form_valid(self, form):
        messages.success(self.request, "編集を更新しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新できませんでした。")
        return redirect('kakeibo:records_top')


class EditIncome(LoginRequiredMixin, OnlyYouIncomeMixin, generic.UpdateView):
    template_name = 'records/edit.html'
    model = Incomes
    form_class = IncomeForm
    success_url = reverse_lazy('kakeibo:records_top')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existed_addition_category'] = list(
            Categories.objects.filter(user_id=self.request.user.id).values_list('id', flat=True))
        return context

    def form_valid(self, form):
        messages.success(self.request, "編集を更新しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新できませんでした。")
        return redirect('kakeibo:records_top')


class EditLatestExpenditure(LoginRequiredMixin, OnlyYouExpenditureMixin, generic.UpdateView):
    template_name = 'records/edit.html'
    model = Expenditures
    form_class = ExpenditureForm
    success_url = reverse_lazy('kakeibo:records_latest_registration_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existed_addition_category'] = list(
            Categories.objects.filter(user_id=self.request.user.id).values_list('id', flat=True))
        return context

    def form_valid(self, form):
        messages.success(self.request, "編集を更新しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新できませんでした。")
        return redirect('kakeibo:records_latest_registration_list')


class EditLatestIncome(LoginRequiredMixin, OnlyYouIncomeMixin, generic.UpdateView):
    template_name = 'records/edit.html'
    model = Incomes
    form_class = IncomeForm
    success_url = reverse_lazy('kakeibo:records_latest_registration_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existed_addition_category'] = list(
            Categories.objects.filter(user_id=self.request.user.id).values_list('id', flat=True))
        return context

    def form_valid(self, form):
        messages.success(self.request, "編集を更新しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新できませんでした。")
        return redirect('kakeibo:records_latest_registration_list')


class LatestRegistrationList(LoginRequiredMixin, generic.ListView):
    template_name = 'records/latest_registration_list.html'
    context_object_name = 'records'
    paginate_by = 20

    def get_queryset(self):
        expenditure_record = Expenditures.objects.order_by('-created_at').filter(user_id=self.request.user.id,
                                                                                 deleted=False).select_related(
            'category')[
                             :100]
        income_record = Incomes.objects.order_by('-created_at').filter(user_id=self.request.user.id,
                                                                       deleted=False).select_related('category')[
                        :100]
        return sorted(chain(expenditure_record, income_record), key=lambda instance: instance.created_at, reverse=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenditure_categories'] = Categories.objects.filter(label='expenditure').values_list('id', flat=True)
        context['income_categories'] = Categories.objects.filter(label='income').values_list('id', flat=True)
        return context


def delete_income(request, pk):
    if _delete_income(request, pk):
        messages.success(request, '削除しました。')
        return redirect('kakeibo:records_top')


def delete_expenditure(request, pk):
    if _delete_expenditure(request, pk):
        messages.success(request, '削除しました。')
        return redirect('kakeibo:records_top')


def delete_latest_income(request, pk):
    if _delete_income(request, pk):
        messages.success(request, '削除しました。')
        return redirect('kakeibo:records_latest_registration_list')


def delete_latest_expenditure(request, pk):
    if _delete_expenditure(request, pk):
        messages.success(request, '削除しました。')
        return redirect('kakeibo:records_latest_registration_list')


def _validate_search(specified_date):
    return datetime.strptime(specified_date, '%Y-%m-%d')


def _delete_income(request, pk):
    if request.method == 'POST':
        income = Incomes.objects.get(pk=pk, user=request.user)
        income.deleted = True
        income.save()
        return income


def _delete_expenditure(request, pk):
    if request.method == 'POST':
        expenditure = Expenditures.objects.get(pk=pk, user=request.user)
        expenditure.deleted = True
        expenditure.save()
        return expenditure


@transaction.atomic
def records_import(request):
    if 'kakeibo-csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['kakeibo-csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        # NOTE: Skip header.
        next(csv_file)
    try:
        with transaction.atomic():
            for line in csv_file:
                if line[0] == "収入":
                    category = Categories.objects.filter(label='income', name=line[1], user=request.user).first()
                    if not category:
                        category = Categories.objects.create(label='income', name=line[1], user=request.user)
                    Expenditures.objects.create(user=request.user, category=category, event_date=line[2],
                                                amount=int(line[3]), memo=line[4])
                if line[0] == "支出":
                    category = Categories.objects.filter(label='expenditure', name=line[1], user=request.user).first()
                    if not category:
                        category = Categories.objects.create(label='expenditure', name=line[1], user=request.user)
                    Expenditures.objects.create(user=request.user, category=category, event_date=line[2],
                                                amount=int(line[3]), memo=line[4])
            messages.success(request, 'インポートに成功しました。')
    except:
        messages.error(request, "インポートに失敗しました。")
    return redirect('kakeibo:records_top')
