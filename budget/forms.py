from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import ExpenditurePlans


class ExpenditurePlanAmountForm(forms.ModelForm):
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 0, 'max': 9999999999999, 'value': 0, 'class': 'appearance-none block '
                                                                                             'w-full bg-gray-200 '
                                                                                             'text-gray-700 border '
                                                                                             'border-gray-200 rounded '
                                                                                             'py-3 px-4 leading-tight '
                                                                                             'focus:outline-none '
                                                                                             'focus:bg-white'}),
        required=False,
    )

    class Meta:
        model = ExpenditurePlans
        fields = ['amount']


class ExpenditurePlanForm(forms.ModelForm):
    amount = forms.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999999999)
        ],
        widget=forms.NumberInput(attrs={'placeholder': ''}),
        required=False,
    )
    category = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": ""}, ),
    )
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': '日付'}),
    )

    def __init__(self, category_id, event_date, amount, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ExpenditurePlans
        fields = ['amount', 'category', 'event_date']
