from django.contrib.auth.mixins import UserPassesTestMixin

from kakeibo.models import Income, Expenditure


class OnlyYouMixin(UserPassesTestMixin):
    """
    login user only access.
    """

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class OnlyYouIncomeMixin(UserPassesTestMixin):
    """
    login user only register own income.
    """
    raise_exception = True

    def test_func(self):
        return Income.objects.filter(id=self.kwargs['pk'], user_id=self.request.user.id, deleted=False).exists()


class OnlyYouExpenditureMixin(UserPassesTestMixin):
    """
    login user only register own expenditure.
    """
    raise_exception = True

    def test_func(self):
        return Expenditure.objects.filter(id=self.kwargs['pk'], user_id=self.request.user.id, deleted=False).exists()
