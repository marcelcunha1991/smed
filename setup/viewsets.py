import decimal

from django.db.models import Count
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
    def listar_procedimentos(self, request, pk):

        try:
            externo = Procedimento.objects.filter(setup__processo=pk, setup__tipo=1)
            interno = Procedimento.objects.filter(setup__processo=pk, setup__tipo=2)

            serializer1 = ProcedimentoShortSerializer(externo, many=True)
            serializer2 = ProcedimentoShortSerializer(interno, many=True)

            data = {
                'setup_externo': serializer1.data,
                'setup_interno': serializer2.data
            }

        except Exception as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)


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
        # procedimento.tempo_realizado = request.data.get('tempo_realizado', procedimento.tempo_realizado)
        # procedimento.observacao = request.data.get('observacao', procedimento.observacao)

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

        serializer = ProcedimentoShortSerializer(procedimento)

        if decimal.Decimal(procedimento.tempo_realizado) <= procedimento.tempo_estimado:
            procedimento.status = 3
        else:
            procedimento.status = 4

        procedimento.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def finalizar_com_justificativa(self, request, pk):
        procedimento = self.get_object()
        procedimento.tempo_realizado = request.data.get('tempo_realizado', procedimento.tempo_realizado)
        procedimento.observacao = request.data.get('observacao', procedimento.observacao)

        procedimento.status = 5
        procedimento.save()

        serializer = ProcedimentoDetailsSerializer(procedimento)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def listar_etapa_cargo(self, request):
        op = self.request.query_params.get('op', None)
        setor = self.request.query_params.get('setor', None)
        status_ = '1'

        procedimento = Procedimento.objects.values(
            'setup__processo__id',
            'setup__processo__descricao',
            'setup__processo__maquina__descricao',
            'setup__processo__op__descricao',
            'setup__processo__etapa',
            'setup__processo__hora_inicio',
            'setup__processo__gerente__name',
            'setor__descricao'
        ) \
            .annotate(qtde_atividades=Count('setor')).filter(
            setor=setor,
            status=status_
            # setup__processo__op=op
        )
        try:
            if op:
                procedimento = procedimento.filter(setup__processo__op=op)
        except Exception as e:
            mensagem = {'error': e.args[0]}
            return Response(mensagem, status=404)

        return Response({'etapa_processo': procedimento}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def verificar_procedimento_aberto(self, request):
        user = self.request.query_params.get('operador', None)

        try:
            procedimento = Procedimento.objects.filter(operador=user, status=2)
            if not procedimento:  # Verifica se a lista for zero, vazio ou false
                return Response({'menssage': 'Empty List'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProcedimentoShortSerializer(procedimento, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'menssage': e.args[0]}, status=status.HTTP_404_NOT_FOUND)
