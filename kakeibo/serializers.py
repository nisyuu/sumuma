from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from .models import Categories, Incomes, Expenditures


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'label', 'name']


class NestedCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']


class IncomesSerializer(FlexFieldsModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.filter(label='expenditure'))

    class Meta:
        model = Incomes
        fields = ['id', 'amount', 'event_date', 'memo', 'category', 'created_at', 'updated_at']
        expandable_fields = {'category': NestedCategoriesSerializer}


class ExpendituresSerializer(FlexFieldsModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.filter(label='expenditure'))

    class Meta:
        model = Expenditures
        fields = ['id', 'amount', 'event_date', 'memo', 'category', 'created_at', 'updated_at']
        expandable_fields = {'category': NestedCategoriesSerializer}
