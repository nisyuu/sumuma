import uuid
from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import redirect
from django.views import generic

from kakeibo.models import Expenditures, Categories
from .forms import ExpenditurePlanAmountForm
from .models import ExpenditurePlans


class Top(LoginRequiredMixin, generic.TemplateView):
    template_name = 'budget/top.html'

    def get(self, request, **kwargs):
        year_and_month = date.today()
        beginning_of_month = _get_beginning_of_month(year_and_month)
        end_of_month = _get_end_of_month(year_and_month)

        if request.GET and not request.GET.get('year_and_month') == year_and_month.strftime('%Y-%m'):
            year_and_month = _validate_search(request)
            if not year_and_month:
                return redirect('budget:top')
            beginning_of_month = _get_beginning_of_month(year_and_month)
            end_of_month = _get_end_of_month(year_and_month)
            year_and_month = _get_end_of_month(year_and_month)

        expenditure_plans = ExpenditurePlans.objects.filter(
            user_id=self.request.user.id,
            event_date=beginning_of_month
        )
        expenditure_condition = []
        sum_budget = 0
        sum_expenditure = 0
        sum_balance = 0
        for expenditure_plan in expenditure_plans:
            expenditure = Expenditures.objects.filter(
                user_id=self.request.user.id,
                category_id=expenditure_plan.category_id,
                event_date__range=[beginning_of_month, end_of_month],
                deleted=False
            ).aggregate(sum_amount=Sum('amount'))['sum_amount']

            if not expenditure:
                expenditure = 0

            expenditure_condition.append({
                'category_name': expenditure_plan.category.name,
                'budget': expenditure_plan.amount,
                'expenditure': expenditure,
                'balance': expenditure_plan.amount - expenditure
            })
            sum_budget += expenditure_plan.amount
            sum_expenditure += expenditure
            sum_balance += expenditure_plan.amount - expenditure

        last_day = int(end_of_month.strftime('%d'))
        ave = sum_budget / last_day
        this_day_ave_accumulation = 0
        straight_line = []
        event_date = []
        for i in range(last_day):
            back_date = end_of_month - timedelta(i)
            event_date.append('{}/{}'.format(back_date.month, back_date.day))
            this_day_ave_accumulation += ave
            straight_line.append(this_day_ave_accumulation)

        expenditure_records = []
        expenditure = Expenditures.objects.filter(
            user_id=self.request.user.id,
            event_date__range=[beginning_of_month, year_and_month],
            deleted=False
        )

        if expenditure_plans:
            for count_back_day in range(0, int(year_and_month.strftime('%d'))):
                back_date = year_and_month - timedelta(count_back_day)
                sum_expenditure = expenditure.filter(event_date=back_date).aggregate(sum_amount=Sum('amount'))[
                    'sum_amount']
                if bool(sum_expenditure):
                    expenditure_records.append(sum_expenditure)
                else:
                    expenditure_records.append(0)
            expenditure_records.reverse()

            expenditure_accumulation = 0
            for i, expenditure in enumerate(expenditure_records):
                expenditure_accumulation += expenditure
                expenditure_records[i] = expenditure_accumulation
        event_date.reverse()

        context = {
            'this_month': event_date,
            'year_and_month': year_and_month.strftime('%Y-%m'),
            'straight_line': straight_line,
            'expenditure_records': expenditure_records,
            'expenditure_condition': expenditure_condition,
            'sum_budget': sum_budget,
            'sum_expenditure': sum_expenditure,
            'sum_balance': sum_balance,
        }

        return self.render_to_response(context)


class Create(LoginRequiredMixin, generic.TemplateView):
    template_name = 'budget/create.html'

    def get_context_data(self, **kwargs):
        event_date = _validate_search(self.request)
        if not event_date:
            return redirect('budget:top')
        category_ids = Categories.objects.filter(user_id=self.request.user.id).values_list('id', flat=True)
        form = ExpenditurePlanAmountForm()
        context = {
            'year_and_month': event_date.strftime('%Y-%m-%d'),
            'categories': Categories.objects.filter(id__in=category_ids, label='expenditure'),
            'form': form,
        }
        return context


class Edit(LoginRequiredMixin, generic.TemplateView):
    template_name = 'budget/edit.html'

    def get_context_data(self, **kwargs):
        event_date = _validate_search(self.request)
        plan_each_categories = ExpenditurePlans.objects.filter(event_date=event_date.strftime('%Y-%m-%d'))
        if not event_date:
            return redirect('budget:top')
        context = {
            'year_and_month': event_date.strftime('%Y-%m-%d'),
            'plan_each_categories': plan_each_categories,
        }
        return context


@transaction.atomic
def expenditure_plan_save(request):
    budget = ExpenditurePlans.objects.filter(user_id=request.user.id,
                                             event_date=request.POST.get('year_and_month')).first()
    if budget:
        target_date = datetime.strptime(request.POST.get('year_and_month'), '%Y-%m-%d').strftime('%m月')
        messages.error(request, target_date + "の支出予算登録に失敗しました。")
        return redirect('budget:top')
    event_date = request.POST.get('year_and_month')
    all_amount = request.POST.getlist('amount')
    if request.method != 'POST':
        messages.error(request, "登録に失敗しました。")
    try:
        with transaction.atomic():
            for i, category_id in enumerate(request.POST.getlist('category_ids')):
                ExpenditurePlans.objects.create(user_id=request.user.id, category_id=category_id, event_date=event_date,
                                                amount=all_amount[i])
            messages.success(request, "支出計画を登録しました。")
    except:
        messages.error(request, "登録に失敗しました。")
    return redirect('budget:top')


@transaction.atomic
def expenditure_plan_update(request):
    event_date = request.POST.get('year_and_month')
    all_amount = request.POST.getlist('amount')
    if request.method != 'POST':
        messages.error(request, "編集に失敗しました。")
        return redirect('budget:top')
    try:
        with transaction.atomic():
            for i, category_id in enumerate(request.POST.getlist('category_ids')):
                expenditure_plan = ExpenditurePlans.objects.filter(
                    user_id=request.user.id,
                    category_id=category_id,
                    event_date=event_date).first()
                if expenditure_plan:
                    expenditure_plan.amount = all_amount[i]
                    expenditure_plan.save()
                else:
                    ExpenditurePlans.objects.create(user_id=request.user.id, category_id=category_id,
                                                    event_date=event_date,
                                                    amount=all_amount[i])
            messages.success(request, "支出計画を編集しました。")
    except:
        messages.error(request, "編集に失敗しました。")
    return redirect('budget:top')


@transaction.atomic
def copy_last_month_expenditure_plans(request):
    if request.method != 'POST':
        messages.error(request, "登録に失敗しました。")

    user = request.user
    year_and_month = request.POST.get('year_and_month')
    last_month = datetime.strptime(year_and_month, '%Y-%m') + timedelta(days=-1)
    last_month_budget_plans = ExpenditurePlans.objects.filter(user=user, event_date=last_month)
    categories = Categories.objects.filter(user=user, label='expenditure')

    if last_month_budget_plans:
        try:
            with transaction.atomic():
                for category in categories:
                    last_month_budget_plan = last_month_budget_plans.get(category=category)
                    ExpenditurePlans.objects.create(user=user, category=category,
                                                    event_date=last_month_budget_plan.event_date,
                                                    amount=last_month_budget_plan.amount)
                messages.success(request, "前月の支出計画から複製しました。")
        except:
            messages.error(request, " 。")
    return redirect('budget:top')


# setting the submit token
def set_submit_token(request):
    submit_token = str(uuid.uuid4())
    request.session['submit_token'] = submit_token
    return submit_token


# prevent the multiple submit
def exists_submit_token(request):
    token_in_request = request.POST.get('submit_token')
    token_in_session = request.session.pop('submit_token', None)

    if not token_in_request:
        return False
    if not token_in_session:
        return False

    return token_in_request == token_in_session


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
        return year_and_month
    except:
        messages.error(request, '正しく入力してください。')
        return False
