from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from kakeibo.models import Expenditures, Categories

User = get_user_model()


class ToDo(models.Model):
    name = models.TextField(_('memo'), max_length=100, help_text=_('Please enter the name.'))
    amount = models.BigIntegerField(_('amount'), blank=True, null=True)
    event_date = models.DateField(
        _('event date'),
        blank=True,
        null=True,
        help_text=_('Please enter the event date.')
    )
    memo = models.TextField(_('memo'), max_length=1000, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_bought = models.BooleanField(_('is bought'), default=False)
    is_registered = models.BooleanField(_('is registered'), default=False)
    expenditure = models.ForeignKey(Expenditures, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)
