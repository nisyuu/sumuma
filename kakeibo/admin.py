from django.contrib import admin

from .models import Categories, Incomes, Expenditures


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    list_filter = ['user']


class IncomesAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_date', 'memo', 'amount', 'user']
    list_filter = ['user']


class ExpendituresAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_date', 'memo', 'amount', 'user']
    list_filter = ['user']


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Incomes, IncomesAdmin)
admin.site.register(Expenditures, ExpendituresAdmin)
