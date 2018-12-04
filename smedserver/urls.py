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

from accounts.viewsets import UserViewSet, LoginViewSet, LogoutViewSet, index
from maquinas.viewsets import MaquinasViewSet
from setup.viewsets import OrdemProcessoViewSet, EtapaProcessoViewSet, SetupViewSet, ProcedimentoViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, base_name='User')
router.register(r'maquinas', MaquinasViewSet)
router.register(r'ordem-processo', OrdemProcessoViewSet)
router.register(r'etapa-processo', EtapaProcessoViewSet)
router.register(r'setup', SetupViewSet)
router.register(r'procedimento', ProcedimentoViewSet, base_name='Procedimento')

urlpatterns = [
    path('api/', include(router.urls)),
    path('user/login/', LoginViewSet.as_view()),
    path('user/logout/', LogoutViewSet.as_view()),
    path('', index),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
