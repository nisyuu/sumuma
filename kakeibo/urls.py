from django.urls import path

from .views import kakeibo, records

app_name = 'kakeibo'

urlpatterns = [
    path('', kakeibo.Top.as_view(), name='top'),
    path('create-income/', kakeibo.CreateIncome.as_view(), name='create_income'),
    path('create-expenditure/', kakeibo.CreateExpenditure.as_view(), name='create_expenditure'),
    path('edit-income/<int:pk>/', kakeibo.EditIncome.as_view(), name='edit_income'),
    path('edit-expenditure/<int:pk>/', kakeibo.EditExpenditure.as_view(), name='edit_expenditure'),
    path('delete-income/<int:pk>/', kakeibo.delete_income, name='delete_income'),
    path('delete-expenditure/<int:pk>/', kakeibo.delete_expenditure, name='delete_expenditure'),
    path('categories/', kakeibo.CategoryIndex.as_view(), name='categories'),
    path('create-category/', kakeibo.CreateCategory.as_view(), name='create_category'),
    path('delete-category/<int:pk>/', kakeibo.DeleteCategory.as_view(), name='delete_category'),
    # NOTE: records urls
    path('records/', records.Top.as_view(), name='records_top'),
    path('records/edit-income/<int:pk>/', records.EditIncome.as_view(), name='records_edit_income'),
    path('records/edit-expenditure/<int:pk>/', records.EditExpenditure.as_view(), name='records_edit_expenditure'),
    path("records/delete-income/<int:pk>/", records.delete_income, name='records_delete_income'),
    path("records/delete-expenditure/<int:pk>/", records.delete_expenditure, name='records_delete_expenditure'),
    path('records/latest-registration_list/', records.LatestRegistrationList.as_view(),
         name='records_latest_registration_list'),
    path('records/edit-latest-income/<int:pk>/', records.EditLatestIncome.as_view(), name='records_edit_latest_income'),
    path('records/edit-latest-expenditure/<int:pk>/', records.EditLatestExpenditure.as_view(),
         name='records_edit_latest_expenditure'),
    path("records/delete-latest-income/<int:pk>/", records.delete_latest_income, name='records_delete_latest_income'),
    path("records/delete-latest-expenditure/<int:pk>/", records.delete_latest_expenditure,
         name='records_delete_latest_expenditure'),
    path("records-export/", records.records_export, name='records_export'),
    path("records_import/", records.records_import, name='records_import'),
]
