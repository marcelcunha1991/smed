import decimal

from datetime import datetime
from django.utils import timezone
import pytz

from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from setup.models import EtapaProcesso, Procedimento, OrdemProcesso
from rest_framework.response import Response

from setup.serializers import (
    EtapaProcessoSerializer,
    # SetupSerializer,
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


class ProcedimentoViewSet(ModelViewSet):
    serializer_class = ProcedimentoShortSerializer

    def get_queryset(self):
        processo_id = self.request.query_params.get('processo_id', None)
        setor_id = self.request.data.get('setor_id', None)
        setor_nome = self.request.data.get('setor_nome', None)

        queryset = Procedimento.objects.all()

        if setor_id or setor_nome:
            queryset = queryset.filter(setor=setor_id) | queryset.filter(setor__descricao=setor_nome)
        if processo_id:
            queryset = queryset.filter(processo=processo_id)

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
        procedimento.descricao = request.data.get('descricao', procedimento.descricao)
        procedimento.tempo_estimado = request.data.get('tempo_estimado', procedimento.tempo_estimado)
        procedimento.status = request.data.get('status', procedimento.status)

        try:
            # Se estiver sendo passado o parametro operador
            # a atividade esta sendo inicado, logo, o status muda para "Realizando"
            operador = request.data.get('operador', None)
            if operador:
                operador_id = User.objects.get(id=operador)
                procedimento.operador = operador_id
                procedimento.status = 2
        except Exception as e:
            print('Erro ao tentar salvar usuario ' + e.args[0])

        procedimento.save()
        serializer = ProcedimentoShortSerializer(procedimento)
        return Response(serializer.data)

    # Verifica qual o status da atividade anterior a atual.
    @action(methods=['get'], detail=True)
    def verify_status_pre(self, request):
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

    @action(methods=['post'], detail=True)
    def iniciar_procedimento(self, request, pk):
        procedimento = self.get_object()
        operador = request.data.get('operador', None)
        hora_inicio = request.data.get('hora_inicio', None)

        if not hora_inicio:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            procedimento.hora_inicio = hora_inicio
            operador_id = User.objects.get(id=operador)
            procedimento.operador = operador_id
            procedimento.status = 2  # status = Realizando
            procedimento.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'mensage': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def finalizar_procedimento(self, request, pk):
        procedimento = self.get_object()

        procedimento.hora_fim = request.data.get('hora_fim', None)
        procedimento.status = 3

        try:
            inicio = procedimento.hora_inicio.strftime("%Y-%m-%d %H:%M:%S")
            data_inicio = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
            data_fim = datetime.strptime(procedimento.hora_fim, "%Y-%m-%d %H:%M:%S")
            result = (data_fim - data_inicio).seconds

            procedimento.tempo_realizado = result * 1000
            procedimento.save()
            serializer = ProcedimentoShortSerializer(procedimento)

            self.verificar_procedimento(procedimento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            msg = e.args[0]
            return Response({'mensage': msg}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def finalizar_com_justificativa(self, request, pk):
        procedimento = self.get_object()

        procedimento.hora_fim = request.data.get('hora_fim', None)
        procedimento.status = request.data.get('status', None)
        procedimento.observacao = request.data.get('observacao', None)

        try:
            inicio = procedimento.hora_inicio.strftime("%Y-%m-%d %H:%M:%S")
            data_inicio = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
            data_fim = datetime.strptime(procedimento.hora_fim, "%Y-%m-%d %H:%M:%S")
            result = (data_fim - data_inicio).seconds

            procedimento.tempo_realizado = result * 1000
            procedimento.save()
            serializer = ProcedimentoShortSerializer(procedimento)

            self.verificar_procedimento(procedimento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            msg = e.args[0]
            return Response({'mensage': msg}, status=status.HTTP_400_BAD_REQUEST)

    def verificar_procedimento(self, procedimento):
        pro = Procedimento.objects.filter(status=1) | Procedimento.objects.filter(status=2)
        # Se retornar vazio, nao existem atividades pendentes
        # # logo, o status do processo deve ser alterado para "finalizado"
        if not pro:
            processo_id = procedimento.processo.id
            etapa = EtapaProcesso.objects.get(id=processo_id)
            etapa.status = 2
            etapa.save()

    # TODO mudar este método usando o query_params.get()
    # procedimento/{id}/listar_procedimento/
    # procedimento/listar_procedimento/?processo_id={?}
    @action(methods=['get'], detail=True)
    def listar_procedimentos(self, request, pk):

        queryset = Procedimento.objects.filter(processo=pk)

        try:
            if not queryset:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:

                externo = queryset.filter(tipo=1)
                interno = queryset.filter(tipo=2)

                serializer1 = ProcedimentoShortSerializer(externo, many=True)
                serializer2 = ProcedimentoShortSerializer(interno, many=True)

                data = {
                    'setup_externo': serializer1.data,
                    'setup_interno': serializer2.data
                }
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def listar_etapa_cargo(self, request):
        op = self.request.query_params.get('op', None)
        setor = self.request.query_params.get('setor', None)

        try:
            procedimento = Procedimento.objects.values(
                'processo__id',
                'processo__descricao',
                'processo__maquina__descricao',
                'processo__op__descricao',
                'processo__etapa',
                'processo__hora_inicio',
                'processo__gerente__name',
            ).annotate(qtde_atividades=Count('setor')).filter(
                setor=setor,
                status=1
            )
            if op:
                procedimento = procedimento.filter(processo__op=op)

            if not procedimento:
                return Response({'message': 'List is empty or null'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'etapa_processo': procedimento}, status=status.HTTP_200_OK)
        except Exception as e:
            mensagem = {'error': e.args[0]}
            return Response(mensagem, status=404)

    @action(methods=['get'], detail=False)
    def verificar_procedimento_aberto(self, request):
        user = self.request.query_params.get('operador', None)

        try:
            procedimento = Procedimento.objects.filter(operador=user, status=2)
            if not procedimento:  # Verifica se a lista for zero, vazio ou false
                return Response({'menssage': 'Empty List'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProcedimentoDetailsSerializer(procedimento, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'menssage': e.args[0]}, status=status.HTTP_404_NOT_FOUND)
