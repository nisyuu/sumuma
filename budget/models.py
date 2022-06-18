from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from kakeibo.models import Categories

User = get_user_model()


class ExpenditurePlans(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    event_date = models.DateField(default=timezone.now)
    amount = models.BigIntegerField(default=0, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)
