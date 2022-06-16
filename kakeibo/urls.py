from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('create-income/', views.CreateIncome.as_view(), name='create_income'),
    path('create-expenditure/', views.CreateExpenditure.as_view(), name='create_expenditure'),
    path('edit-income/<int:pk>/', views.EditIncome.as_view(), name='edit_income'),
    path('edit-expenditure/<int:pk>/', views.EditExpenditure.as_view(), name='edit_expenditure'),
    path('delete-income/<int:pk>/', views.delete_income, name='delete_income'),
    path('delete-expenditure/<int:pk>/', views.delete_expenditure, name='delete_expenditure'),
    path('categories/', views.CategoryIndex.as_view(), name='categories'),
    path('create-category/', views.CreateCategory.as_view(), name='create_category'),
    path('delete-category/<int:pk>/', views.DeleteCategory.as_view(), name='delete_category'),
]