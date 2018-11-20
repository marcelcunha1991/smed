"""smedserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers

from core import views as urls_core
from accounts.api.viewsets import UserViewSet
from maquinas.api.viewsets import MaquinasViewSet
from setup.api.viewsets import ProcessoViewSet, SetupViewSet, ProcedimentoViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'maquinas', MaquinasViewSet)
router.register(r'processo', ProcessoViewSet)
router.register(r'setup', SetupViewSet)
router.register(r'procedimento', ProcedimentoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', urls_core.index),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
