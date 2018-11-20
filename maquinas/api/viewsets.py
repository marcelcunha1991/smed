from rest_framework.viewsets import ModelViewSet


from maquinas.models import Tipo, Maquinas
from maquinas.api.serializers import TipoSerializer, MaquinasSerializer


class MaquinasViewSet(ModelViewSet):
    queryset = Maquinas.objects.all()
    serializer_class = MaquinasSerializer


class TipoViewSet(ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer
