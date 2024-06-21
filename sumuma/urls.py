"""sumuma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import environ
from rest_framework import permissions
from rest_framework import routers

from kakeibo.views.api.kakeibo import CategoriesViewSet, IncomesViewSet, ExpendituresViewSet
from sumuma.settings import ADMIN_DASHBOARD_PATH

env = environ.Env()

schema_view = get_schema_view(
    openapi.Info(
        title="SUMUMA API",
        default_version='v1',
        description="SUMUMA Swagger UI",
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'incomes', IncomesViewSet, basename='incomes')
router.register(r'expenditures', ExpendituresViewSet, basename='expenditures')

urlpatterns = [
    path(ADMIN_DASHBOARD_PATH, admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('home.urls')),
    # path('account/', include('account.urls')),
    # path('kakeibo/', include('kakeibo.urls')),
    # path('analyses/', include('analyses.urls')),
    # path('contact/', include('contact.urls')),
    # path('budget/', include('budget.urls')),
    # path('shopping/', include('shopping.urls')),
    # path('lp/', include('lp.urls')),
    # NOTE: api routers
    # path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # NOTE: swagger
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('openapi/', get_schema_view(
    #     title="Your Project",
    #     description="API for all things …",
    #     version="1.0.0"
    # ), name='openapi-schema'),
    # path('swagger-ui/', TemplateView.as_view(
    #     template_name='swagger-ui.html',
    #     extra_context={'schema_url': 'openapi-schema'}
    # ), name='swagger-ui'),
]
