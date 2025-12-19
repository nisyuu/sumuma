from django.test import TestCase
from budget.forms import ExpenditurePlanAmountForm


class BudgetFormsTests(TestCase):
    def test_expenditure_plan_amount_form_valid(self):
        """Test the ExpenditurePlanAmountForm with valid data."""
        form_data = {'amount': 10000}
        form = ExpenditurePlanAmountForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_expenditure_plan_amount_form_zero_valid(self):
        """Test the form is valid with zero amount."""
        form_data = {'amount': 0}
        form = ExpenditurePlanAmountForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_expenditure_plan_amount_form_not_required(self):
        """Test the form is valid even when amount is not provided, as it is not required."""
        form_data = {}
        form = ExpenditurePlanAmountForm(data=form_data)
        self.assertTrue(form.is_valid())
        # The form should provide a cleaned_data value of None if not provided
        self.assertIsNone(form.cleaned_data.get('amount'))