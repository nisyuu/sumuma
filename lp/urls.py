from django.urls import path

from . import views
from django.views.decorators.cache import cache_page

# from django.views.decorators.cache import cache_page

app_name = 'lp'

urlpatterns = [
    path('general/', cache_page(60 * 60 * 2)(views.General.as_view()), name='general'),
]
