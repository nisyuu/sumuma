from django.urls import path
from . import views

app_name = 'shopping'

urlpatterns = [
    path('todo/', views.Top.as_view(), name='top'),
]
