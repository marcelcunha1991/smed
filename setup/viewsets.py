import decimal

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from setup.models import EtapaProcesso, Setup, Procedimento, OrdemProcesso
from rest_framework.response import Response

from setup.serializers import (
    EtapaProcessoSerializer,
    SetupSerializer,
    OrdemProcessoSerializer,
    ProcedimentoShortSerializer, ProcedimentoDetailsSerializer, ProcedimentoStatusSerializer)


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

    # Usar o metodo HTTP PATCH no front-end
    def partial_update(self, request, *args, **kwargs):
        procedimento = self.get_object()

        # TODO Nesse trecho podem ser colocados os campos a serem atualizados quando for necessário
        procedimento.status = request.data.get('status', procedimento.status)
        procedimento.descricao = request.data.get('descricao', procedimento.descricao)
        procedimento.tempo_estimado = request.data.get('tempo_estimado', procedimento.tempo_estimado)
        procedimento.tempo_realizado = request.data.get('tempo_realizado', procedimento.tempo_realizado)
        procedimento.observacao = request.data.get('observacao', procedimento.observacao)

        operador = request.data.get('operador', None)
        if operador is not None:
            if operador != '':
                operador_id = User.objects.get(id=operador)
                procedimento.operador = operador_id

        procedimento.save()
        serializer = ProcedimentoShortSerializer(procedimento)
        return Response(serializer.data)

    # Verifica qual o status da atividade anterior a atual.
    @action(methods=['get'], detail=True)
    def verify_status_pre(self, request, pk):
        if self.get_object().predecessor is not None:
            predecessorId = self.get_object().predecessor.id
            predecessor = Procedimento.objects.get(id=predecessorId)
        else:
            return Response('the object has no predecessor', status=status.HTTP_404_NOT_FOUND)

        serializer = ProcedimentoStatusSerializer(predecessor)

        if predecessor.status is not None:
            if predecessor.status >= 3:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response('The status field is empty', status=status.HTTP_404_NOT_FOUND)

    @action(methods=['POST'], detail=True)
    def finalizar_procedimento(self, request, pk):
        procedimento = self.get_object()
        procedimento.tempo_realizado = request.data.get('tempo_realizado', procedimento.tempo_realizado)

        tempo_calculado = (procedimento.tempo_estimado - decimal.Decimal(procedimento.tempo_realizado))

        if tempo_calculado < 0:
            procedimento.status = 4
        else:
            procedimento.status = 3

        procedimento.save()

        return Response(status=status.HTTP_200_OK)
