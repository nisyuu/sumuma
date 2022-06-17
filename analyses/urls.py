from django.urls import path

from . import views

app_name = 'analyses'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('accumulation', views.Accumulation.as_view(), name='accumulation'),
    path('transition', views.Transition.as_view(), name='transition'),
    path('analyses_by_category', views.AnalysesByCategory.as_view(), name='analyses_by_category'),
    path('search_pie_each_month', views.search_pie_each_month, name='search_pie_each_month'),
    path('search_accumulation_each_month', views.search_accumulation_each_month, name='search_accumulation_each_month'),
    path('search_transition_each_month', views.search_transition_each_month, name='search_transition_each_month'),
    path('search_analyses_by_category_each_month', views.search_analyses_by_category_each_month,
         name='search_analyses_by_category_each_month'),
]
