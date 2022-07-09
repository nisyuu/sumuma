from django.urls import path
from . import views

app_name = 'shopping'

urlpatterns = [
    path('todo/', views.Top.as_view(), name='top'),
    path('create-todo/', views.CreateToDo.as_view(), name='create_todo'),
    path('edit-todo/<int:pk>/', views.EditToDo.as_view(), name='edit_todo'),
    path('delete-todo/<int:pk>/', views.DeleteToDo.as_view(), name='delete_todo'),
]
