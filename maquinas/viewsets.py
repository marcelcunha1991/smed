from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from maquinas.models import Tipo, Maquinas
from maquinas.serializers import TipoSerializer, MaquinasSerializer


class MaquinasViewSet(ModelViewSet):
    queryset = Maquinas.objects.all()
    serializer_class = MaquinasSerializer

    def create(self, request, *args, **kwargs):
        descricao = self.request.data.get('descricao', None)
        # tipo = self.request.data.get('tipo', None)
        statusS = self.request.data.get('status', None)

        try:
            # tipo = Tipo.objects.get(id=tipo)
            maquina = Maquinas.objects.create(
                descricao=descricao,
                # tipo=tipo,
                status=statusS)
            serializer = MaquinasSerializer(maquina)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class TipoViewSet(ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer
