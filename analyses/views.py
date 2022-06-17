from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import generic

from kakeibo.models import Expenditure, Income, Categories


class Top(LoginRequiredMixin, generic.TemplateView):
    template_name = 'analyses/top.html'

    def get(self, request, **kwargs):
        today = date.today()
        categories = Categories.objects.filter(user_id=self.request.user.id)

        expenditures = Expenditure.objects.filter(
            user_id=self.request.user.id,
            event_date__range=[_get_beginning_of_month(today), today],
            deleted=False
        )

        expenditure_records = {}
        for category in categories:
            expenditure = \
                expenditures.filter(category=category).aggregate(sum_amount=Sum('amount'))[
                    'sum_amount']
            if expenditure:
                expenditure_records[category.name] = expenditure

        expenditure_records = dict(sorted(expenditure_records.items(), key=lambda x: -x[1]))
        context = {
            'this_month': today.month,
            'expenditure_or_income_records': expenditure_records,
            'expenditure_sum_amount': list(expenditure_records.values()),
            'expenditure_categories_name': list(expenditure_records.keys()),
            'total_expenditures': sum(expenditure_records.values()),
            'year_and_month': today.strftime('%Y-%m'),
        }
        return self.render_to_response(context)


class Transition(LoginRequiredMixin, generic.TemplateView):
    template_name = 'analyses/transition.html'

    def get_context_data(self, **kwargs):
        today = date.today()
        event_date = []
        expenditure_records = []

        expenditures = Expenditure.objects.filter(
            user_id=self.request.user.id,
            event_date__range=[_get_beginning_of_month(today), today],
            deleted=False
        )

        for count_back_day in range(0, int(today.strftime('%d'))):
            back_date = today - timedelta(count_back_day)
            sum_expenditures = expenditures.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                'sum_amount']
            if bool(sum_expenditures):
                expenditure_records.append(sum_expenditures)
            else:
                expenditure_records.append(0)
            event_date.append('{}/{}'.format(back_date.month, back_date.day))

        event_date.reverse()
        expenditure_records.reverse()

        context = {
            'this_month': today.month,
            'expenditure_or_income_records': expenditure_records,
            'event_date': event_date,
            'total_amount': sum(expenditure_records),
            'transition_list': kakeibo_detail_list(event_date, expenditure_records),
            'year_and_month': today.strftime('%Y-%m'),
        }
        return context


class Accumulation(LoginRequiredMixin, generic.TemplateView):
    template_name = 'analyses/accumulation.html'

    def get_context_data(self, **kwargs):
        today = date.today()
        event_date = []
        expenditure_records = []

        expenditures = Expenditure.objects.filter(
            user_id=self.request.user.id,
            event_date__range=[_get_beginning_of_month(today), today],
            deleted=False
        )

        for count_back_day in range(0, int(today.strftime('%d'))):
            back_date = today - timedelta(count_back_day)
            sum_expenditure = expenditures.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                'sum_amount']
            if bool(sum_expenditure):
                expenditure_records.append(sum_expenditure)
            else:
                expenditure_records.append(0)
            event_date.append('{}/{}'.format(back_date.month, back_date.day))
        event_date.reverse()
        expenditure_records.reverse()

        expenditures_accumulation = 0
        for i, expenditures in enumerate(expenditure_records):
            expenditures_accumulation += expenditures
            expenditure_records[i] = expenditures_accumulation

        context = {
            'accumulation_list': kakeibo_detail_list(event_date, expenditure_records),
            'expenditure_or_income_records': expenditure_records,
            'event_date': event_date,
            'year_and_month': today.strftime('%Y-%m'),
        }
        return context


class AnalysesByCategory(LoginRequiredMixin, generic.TemplateView):
    template_name = 'analyses/analyses_by_category.html'

    def get_context_data(self, **kwargs):
        today = date.today()
        categories = Categories.objects.filter(user_id=self.request.user.id)

        event_date = make_date_series(today)
        expenditure_records = {}
        for category in categories:
            expenditure_records[category.name] = []
            expenditures = Expenditure.objects.filter(
                user_id=self.request.user.id,
                category=category,
                event_date__range=[_get_beginning_of_month(today), today],
                deleted=False
            )
            for count_back_day in range(0, int(today.strftime('%d'))):
                back_date = today - timedelta(count_back_day)
                sum_expenditures = expenditures.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                    'sum_amount']
                if bool(sum_expenditures):
                    expenditure_records[category.name].append(sum_expenditures)
                else:
                    expenditure_records[category.name].append(0)

            if len(set(expenditure_records[category.name])) == 1:
                expenditure_records.pop(category.name)
            else:
                expenditure_records[category.name].reverse()

        context = {
            'categories': list(expenditure_records.keys()),
            'expenditure_or_income_records': list(expenditure_records.values()),
            'event_date': event_date,
            'year_and_month': today.strftime('%Y-%m'),
        }
        return context


def search_pie_each_month(request):
    year_and_month = _validate_search(request)
    selected_expenditure_or_income = request.GET.get('expenditure_or_income')
    if year_and_month == False or (date.today().strftime('%Y-%m') == year_and_month.strftime(
            '%Y-%m') and selected_expenditure_or_income == 'expenditure'):
        return redirect('analyses:top')
    beginning_of_month = _get_beginning_of_month(year_and_month)
    end_of_month = _get_end_of_month(year_and_month)

    if selected_expenditure_or_income == 'expenditure':
        expenditure_or_income = Expenditure.objects.filter(
            user_id=request.user.id,
            event_date__range=[beginning_of_month, end_of_month],
            deleted=False
        )
    else:
        expenditure_or_income = Income.objects.filter(
            user_id=request.user.id,
            event_date__range=[beginning_of_month, end_of_month],
            deleted=False
        )

    categories = Categories.objects.filter(user_id=request.user.id)
    expenditures_or_income_records = {}
    for category in categories:
        if selected_expenditure_or_income == 'expenditure':
            expenditures_or_income = \
                expenditure_or_income.filter(category=category).aggregate(
                    sum_amount=Sum('amount'))[
                    'sum_amount']
        else:
            expenditures_or_income = \
                expenditure_or_income.filter(category=category).aggregate(
                    sum_amount=Sum('amount'))[
                    'sum_amount']

        if expenditures_or_income:
            expenditures_or_income_records[category.name] = expenditures_or_income

    expenditures_or_income_records = dict(sorted(expenditures_or_income_records.items(), key=lambda x: -x[1]))
    if selected_expenditure_or_income == 'expenditure':
        pie_graph_name = '支出'
    else:
        pie_graph_name = '収入'

    context = {
        'expenditure_or_income': selected_expenditure_or_income,
        'expenditure_or_income_records': expenditures_or_income_records,
        'expenditure_sum_amount': list(expenditures_or_income_records.values()),
        'expenditure_categories_name': list(expenditures_or_income_records.keys()),
        'pie_graph_name': pie_graph_name,
        'total_expenditures': sum(expenditures_or_income_records.values()),
        'this_month': year_and_month.month,
        'year_and_month': request.GET.get('year_and_month'),
    }
    return render(request, 'analyses/top.html', context)


def search_accumulation_each_month(request):
    year_and_month = _validate_search(request)
    selected_expenditure_or_income = request.GET.get('expenditure_or_income')
    if year_and_month == False or (date.today().strftime('%Y-%m') == year_and_month.strftime(
            '%Y-%m') and selected_expenditure_or_income == 'expenditure'):
        return redirect('analyses:accumulation')
    end_of_month = _get_end_of_month(year_and_month)

    if selected_expenditure_or_income == 'expenditure':
        expenditure_or_income = Expenditure.objects.filter(
            user_id=request.user.id,
            event_date__range=[_get_beginning_of_month(year_and_month), end_of_month],
            deleted=False
        )
    else:
        expenditure_or_income = Income.objects.filter(
            user_id=request.user.id,
            event_date__range=[_get_beginning_of_month(year_and_month), end_of_month],
            deleted=False
        )

    event_date = []
    expenditures_or_income_records = []
    for count_back_day in range(0, int(end_of_month.strftime('%d'))):
        back_date = end_of_month - timedelta(count_back_day)
        if selected_expenditure_or_income == 'expenditure':
            expenditures_or_income = \
                expenditure_or_income.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                    'sum_amount']
        else:
            expenditures_or_income = \
                expenditure_or_income.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                    'sum_amount']
        if bool(expenditures_or_income):
            expenditures_or_income_records.append(expenditures_or_income)
        else:
            expenditures_or_income_records.append(0)
        event_date.append('{}/{}'.format(back_date.month, back_date.day))

    event_date.reverse()
    expenditures_or_income_records.reverse()

    expenditures_accumlation = 0
    for i, expenditures_or_income in enumerate(expenditures_or_income_records):
        expenditures_accumlation += expenditures_or_income
        expenditures_or_income_records[i] = expenditures_accumlation

    context = {
        'accumulation_list': kakeibo_detail_list(event_date, expenditures_or_income_records),
        'expenditure_or_income': selected_expenditure_or_income,
        'expenditure_or_income_records': expenditures_or_income_records,
        'event_date': event_date,
        'year_and_month': request.GET.get('year_and_month'),
    }
    return render(request, 'analyses/accumulation.html', context)


def search_transition_each_month(request):
    year_and_month = _validate_search(request)
    selected_expenditure_or_income = request.GET.get('expenditure_or_income')
    if not year_and_month or (date.today().strftime('%Y-%m') == year_and_month.strftime(
            '%Y-%m') and selected_expenditure_or_income == 'expenditure'):
        return redirect('analyses:transition')
    end_of_month = _get_end_of_month(year_and_month)

    if selected_expenditure_or_income == 'expenditure':
        expenditure_or_income = Expenditure.objects.filter(
            user_id=request.user.id,
            event_date__range=[_get_beginning_of_month(year_and_month), end_of_month],
            deleted=False
        )
    else:
        expenditure_or_income = Income.objects.filter(
            user_id=request.user.id,
            event_date__range=[_get_beginning_of_month(year_and_month), end_of_month],
            deleted=False
        )

    event_date = []
    expenditures_or_income_records = []
    for count_back_day in range(0, int(end_of_month.strftime('%d'))):
        back_date = end_of_month - timedelta(count_back_day)
        if selected_expenditure_or_income == 'expenditure':
            expenditures_or_income = \
                expenditure_or_income.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                    'sum_amount']
        else:
            expenditures_or_income = \
                expenditure_or_income.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                    'sum_amount']
        if bool(expenditures_or_income):
            expenditures_or_income_records.append(expenditures_or_income)
        else:
            expenditures_or_income_records.append(0)
        event_date.append('{}/{}'.format(back_date.month, back_date.day))
    event_date.reverse()
    expenditures_or_income_records.reverse()
    context = {
        'expenditure_or_income': selected_expenditure_or_income,
        'expenditure_or_income_records': expenditures_or_income_records,
        'event_date': event_date,
        'this_month': year_and_month.month,
        'total_amount': sum(expenditures_or_income_records),
        'transition_list': kakeibo_detail_list(event_date, expenditures_or_income_records),
        'year_and_month': request.GET.get('year_and_month'),
    }
    return render(request, 'analyses/transition.html', context)


def search_analyses_by_category_each_month(request):
    year_and_month = _validate_search(request)
    selected_expenditure_or_income = request.GET.get('expenditure_or_income')
    if not year_and_month or (date.today().strftime('%Y-%m') == year_and_month.strftime(
            '%Y-%m') and selected_expenditure_or_income == 'expenditure'):
        return redirect('analyses:analyses_by_category')
    end_of_month = _get_end_of_month(year_and_month)
    event_date = make_date_series(end_of_month)
    categories = Categories.objects.filter(user_id=request.user.id)

    expenditures_or_income_records = {}
    for category in categories:
        expenditures_or_income_records[category.name] = []

        if selected_expenditure_or_income == 'expenditure':
            expenditure_or_income = Expenditure.objects.filter(
                user_id=request.user.id,
                category=category,
                event_date__range=[_get_beginning_of_month(year_and_month), end_of_month],
                deleted=False
            )
        else:
            expenditure_or_income = Income.objects.filter(
                user_id=request.user.id,
                category=category,
                event_date__range=[_get_beginning_of_month(year_and_month), end_of_month],
                deleted=False
            )

        for count_back_day in range(0, int(end_of_month.strftime('%d'))):
            back_date = end_of_month - timedelta(count_back_day)
            if selected_expenditure_or_income == 'expenditure':
                expenditures_or_income = \
                    expenditure_or_income.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                        'sum_amount']
            else:
                expenditures_or_income = \
                    expenditure_or_income.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                        'sum_amount']

            if bool(expenditures_or_income):
                expenditures_or_income_records[category.name].append(expenditures_or_income)
            else:
                expenditures_or_income_records[category.name].append(0)

        if len(set(expenditures_or_income_records[category.name])) == 1:
            expenditures_or_income_records.pop(category.name)
        else:
            expenditures_or_income_records[category.name].reverse()

    context = {
        'year_and_month': request.GET.get('year_and_month'),
        'expenditure_or_income': selected_expenditure_or_income,
        'categories': list(expenditures_or_income_records.keys()),
        'expenditure_or_income_records': list(expenditures_or_income_records.values()),
        'event_date': event_date,
    }

    return render(request, 'analyses/analyses_by_category.html', context)


def make_date_series(end_date):
    event_date = []
    for count_back_day in range(0, int(end_date.strftime('%d'))):
        back_date = end_date - timedelta(count_back_day)
        event_date.append('{}/{}'.format(back_date.month, back_date.day))
    event_date.reverse()
    return event_date


def _get_beginning_of_month(year_and_month):
    beginning_of_month = year_and_month.strftime('%Y-%m-01')
    return datetime.strptime(beginning_of_month, '%Y-%m-%d')


def _get_end_of_month(year_and_month):
    beginning_of_month = year_and_month.strftime('%Y-%m-01')
    beginning_of_month = datetime.strptime(beginning_of_month, '%Y-%m-%d')
    end_of_month = beginning_of_month + relativedelta(months=1, days=-1)
    return end_of_month


def _validate_search(request):
    try:
        year_and_month = datetime.strptime(request.GET.get('year_and_month'), '%Y-%m')

        if request.GET.get('expenditure_or_income') not in ['expenditure', 'income']:
            raise Exception

        return year_and_month
    except:
        messages.error(request, '正しく入力してください。')
        return False


def kakeibo_detail_list(event_date, expenditures_or_income_records):
    graph_data_list = []
    for i, _ in enumerate(expenditures_or_income_records):
        graph_data_list.append({'event_date': event_date[i], 'amount': expenditures_or_income_records[i]})
    return graph_data_list
