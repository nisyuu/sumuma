from django.urls import path
from . import views

app_name = 'shopping'

urlpatterns = [
    path('todo/', views.Top.as_view(), name='top'),
    path('create-todo/', views.CreateToDo.as_view(), name='create_todo'),
]
