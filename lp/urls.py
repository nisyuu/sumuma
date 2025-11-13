from django.urls import path

from . import views

app_name = 'lp'

urlpatterns = [
    path('general/', views.General.as_view(), name='general'),
]
