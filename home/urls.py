from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'home'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('terms_of_service/', views.TermsOfService.as_view(), name='terms_of_service'),
    path('privacy_policy/', views.PrivacyPolicy.as_view(), name='privacy_policy'),
]
