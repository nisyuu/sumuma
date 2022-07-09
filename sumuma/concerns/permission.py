from django.contrib.auth.mixins import UserPassesTestMixin

from kakeibo.models import Incomes, Expenditures, Categories
from shopping.models import ToDo


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
        return Incomes.objects.filter(id=self.kwargs['pk'], user_id=self.request.user.id, deleted=False).exists()


class OnlyYouExpenditureMixin(UserPassesTestMixin):
    """
    login user only register own expenditure.
    """
    raise_exception = True

    def test_func(self):
        return Expenditures.objects.filter(id=self.kwargs['pk'], user_id=self.request.user.id, deleted=False).exists()


class OnlyYouCategoryMixin(UserPassesTestMixin):
    """
    login user only register own category.
    """
    raise_exception = True

    def test_func(self):
        return Categories.objects.filter(id=self.kwargs['pk'], user=self.request.user).exists()


class OnlyYouToDoMixin(UserPassesTestMixin):
    """
    login user only register own todo.
    """
    raise_exception = True

    def test_func(self):
        return ToDo.objects.filter(id=self.kwargs['pk'], user=self.request.user).exists()
