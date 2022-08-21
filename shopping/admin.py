from django.contrib import admin

from .models import ToDo


class ToDoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'event_date', 'memo', 'amount', 'user', 'created_at']
    list_filter = ['user']


admin.site.register(ToDo, ToDoAdmin)
