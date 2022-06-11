from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyYouMixin(UserPassesTestMixin):
    """
    login user only access.
    """

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser