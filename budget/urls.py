from django.urls import path

from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('create/', views.Create.as_view(), name='create'),
    path('expenditure-plan-save/', views.expenditure_plan_save, name='expenditure_plan_save'),
    path('edit/', views.Edit.as_view(), name='edit'),
    path('expenditure-plan-update/', views.expenditure_plan_update, name='expenditure_plan_update'),
    path('copy-last-month-expenditure-plans/',
         views.copy_last_month_expenditure_plans,
         name='copy_last_month_expenditure_plans'),
]
