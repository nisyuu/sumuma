from django.core.exceptions import ValidationError
from rest_framework import permissions, viewsets

from kakeibo.models import Categories, Incomes, Expenditures
from kakeibo.serializers import CategoriesSerializer, IncomesSerializer, ExpendituresSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Categories.objects.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomesViewSet(viewsets.ModelViewSet):
    serializer_class = IncomesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Incomes.objects.filter(user=self.request.user).all().order_by('-event_date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpendituresViewSet(viewsets.ModelViewSet):
    serializer_class = ExpendituresSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expenditures.objects.filter(user=self.request.user).all().order_by('-event_date')

    def perform_create(self, serializer):
        category = serializer.validated_data['category']
        if category.user.id is not self.request.user.id:
            raise ValidationError('This category user is not request user.')

        serializer.save(user=self.request.user)
