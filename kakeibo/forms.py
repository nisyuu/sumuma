from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Income, Expenditure, Categories


class IncomeForm(forms.ModelForm):
    amount = forms.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999999999)
        ],
        widget=forms.NumberInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'mb-3 leading-tight focus:outline-none focus:bg-white'}),
    )
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'mb-3 leading-tight focus:outline-none focus:bg-white',
            'x-model': 'datepickerValue',
            '@click': 'showDatepicker = !showDatepicker',
            '@keydown.escape': 'showDatepicker = false',
            'readonly': 'readonly'
        }),
    )
    category = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            "class": "w-full bg-gray-200 border border-gray-200 "
                     "text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white "
                     "focus:border-gray-500pdown"}, ),
        empty_label='カテゴリーを選択してください'
    )
    memo = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'leading-tight focus:outline-none focus:bg-white focus:border-gray-500'}),
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not user and kwargs['initial']['user']:
            user = kwargs['initial']['user']
        self.fields['category'].queryset = \
            Categories.objects.filter(label='income', user=user)

    class Meta:
        model = Income
        fields = ['amount', 'category', 'memo', 'event_date']


class ExpenditureForm(forms.ModelForm):
    amount = forms.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999999999)
        ],
        widget=forms.NumberInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'mb-3 leading-tight focus:outline-none focus:bg-white'}),
    )
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'mb-3 leading-tight focus:outline-none focus:bg-white',
            'x-model': 'datepickerValue',
            '@click': 'showDatepicker = !showDatepicker',
            '@keydown.escape': 'showDatepicker = false',
            'readonly': 'readonly'
        }),
    )
    category = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            "class": "w-full bg-gray-200 border border-gray-200 "
                     "text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white "
                     "focus:border-gray-500pdown"}, ),
        empty_label='カテゴリーを選択してください'
    )
    memo = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'leading-tight focus:outline-none focus:bg-white focus:border-gray-500'}),
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not user and kwargs['initial']['user']:
            user = kwargs['initial']['user']
        self.fields['category'].queryset = \
            Categories.objects.filter(label='expenditure', user=user)

    class Meta:
        model = Expenditure
        fields = ['amount', 'category', 'memo', 'event_date']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border '
                                               'border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none '
                                               'focus:bg-white focus:border-gray-500" id="grid-last-name',
                                      'autofocus': 'true'}),
        required=True
    )

    class Meta:
        model = Categories
        fields = ['label', 'name']
