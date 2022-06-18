from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class KakeiboLabel(models.TextChoices):
    EXPENDITURE = 'expenditure', '支出'
    INCOME = 'income', '収入'


class Categories(models.Model):
    label = models.CharField(_('label'), max_length=16, choices=KakeiboLabel.choices, default=KakeiboLabel.EXPENDITURE)
    name = models.CharField(_('name'), max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Incomes(models.Model):
    amount = models.BigIntegerField(_('amount'), help_text=_('Please enter the amount.'))
    event_date = models.DateField(_('event date'), default=timezone.now, help_text=_('Please enter the event date.'))
    memo = models.TextField(_('memo'), max_length=1000, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, help_text=_('Please enter the category.'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)


class Expenditures(models.Model):
    amount = models.BigIntegerField(_('amount'), help_text=_('Please enter the amount.'))
    event_date = models.DateField(_('event date'), default=timezone.now, help_text=_('Please enter the event date.'))
    memo = models.TextField(_('memo'), max_length=1000, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, help_text=_('Please enter the category.'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)
