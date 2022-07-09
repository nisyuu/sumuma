from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from kakeibo.models import Categories
from .models import ToDo


class ToDoForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'mb-3 leading-tight focus:outline-none focus:bg-white'}),
    )
    amount = forms.IntegerField(
        required=False,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999999999)
        ],
        widget=forms.NumberInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'mb-3 leading-tight focus:outline-none focus:bg-white'}),
    )
    event_date = forms.DateField(
        required=False,
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
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'mb-3 leading-tight focus:outline-none focus:bg-white'}, ),
        empty_label='カテゴリーを選択してください'
    )
    memo = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 '
                     'mb-3 leading-tight focus:outline-none focus:bg-white'}),
    )
    is_bought = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 mb-3'
        })
    )
    is_registered = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 mb-3'
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not user and kwargs['initial']['user']:
            user = kwargs['initial']['user']
        self.fields['category'].queryset = \
            Categories.objects.filter(label='expenditure', user=user)

    class Meta:
        model = ToDo
        fields = ['name', 'amount', 'event_date', 'category', 'memo', 'is_bought', 'is_registered']
