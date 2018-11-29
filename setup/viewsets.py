from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from setup.models import EtapaProcesso, Setup, Procedimento, OrdemProcesso
from rest_framework.response import Response

from setup.serializers import (
    EtapaProcessoSerializer,
    SetupSerializer,
    OrdemProcessoSerializer,
    ProcedimentoShortSerializer, ProcedimentoDetailsSerializer)


class OrdemProcessoViewSet(ModelViewSet):
    queryset = OrdemProcesso.objects.all()
    serializer_class = OrdemProcessoSerializer


class EtapaProcessoViewSet(ModelViewSet):
    queryset = EtapaProcesso.objects.all()
    serializer_class = EtapaProcessoSerializer

    # Lista todos os processos (etapas) associadas a uma OP
    # url etapa-processo/{op_id}/listar_por_op/
    @action(methods=['get'], detail=True)
    def listar_por_op(self, request, pk):
        queryset = EtapaProcesso.objects.filter(op=pk)
        serializer = EtapaProcessoSerializer(queryset, many=True)
        return Response(serializer.data)


class SetupViewSet(ModelViewSet):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer

    @action(methods=['get'], detail=True)
    def listar_por_processo(self, request, **kwargs):
        pass


class ProcedimentoViewSet(ModelViewSet):
    serializer_class = ProcedimentoShortSerializer

    def get_queryset(self):
        setup = self.request.data.get('setup', None)
        setor_id = self.request.data.get('setor_id', None)
        setor_nome = self.request.data.get('setor_nome', None)

        queryset = Procedimento.objects.all()

        if setup:
            queryset = queryset.filter(setup=setup)

        if setor_id or setor_nome:
            queryset = queryset.filter(setor=setor_id) | queryset.filter(setor__descricao=setor_nome)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        procedimento = self.get_object()
        serializer = ProcedimentoDetailsSerializer(procedimento)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return super(ProcedimentoViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        procedimento = self.get_object()

        # TODO Nesse trecho podem ser colocados os campos a serem atualizados quando for necessário
        procedimento.status = request.data.get('status', procedimento.status)
        procedimento.tempo_realizado = request.data.get('tempo_realizado', procedimento.tempo_realizado)
        # Fim

        procedimento.save()
        serializer = ProcedimentoShortSerializer(procedimento)
        return Response(serializer.data)

    # @action(methods=['POST'], detail=True)
    # def update_status(self, request, pk, *args, **kwargs):
    #
    #     pass


"""
Verifica qual status da atividade anterior a atual. 
"""

# @action(methods=['get'], detail=True)
# def verificar_status_pre(self, request, pk):
#
#     procedimento = Procedimento.objects.get(id=pk)
#     if procedimento is not None:
#         serializer = ProcedimentoShortSerializer(procedimento)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response({'response': 'sem predecedente'}, status=status.HTTP_404_NOT_FOUND)
