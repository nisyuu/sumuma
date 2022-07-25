from django.urls import path

from . import views

# from django.views.decorators.cache import cache_page

app_name = 'lp'

urlpatterns = [
    path('general/', views.General.as_view(), name='general'),
]
