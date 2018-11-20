from rest_framework.viewsets import ModelViewSet

from setup.models import Processo, Setup, Procedimento
from setup.api.serializers import ProcessoSerializer, SetupSerializer, ProcedimentoSerializer


class ProcessoViewSet(ModelViewSet):
    queryset = Processo.objects.all()
    serializer_class = ProcessoSerializer


class SetupViewSet(ModelViewSet):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer


class ProcedimentoViewSet(ModelViewSet):
    queryset = Procedimento.objects.all()
    serializer_class = ProcedimentoSerializer
