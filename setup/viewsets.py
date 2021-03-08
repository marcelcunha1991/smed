import sqlite3
from datetime import datetime, timedelta

from django.db.models import Count
from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import User, Cargo
from maquinas.models import Maquinas
from setup.models import EtapaProcesso, Procedimento, OrdemProcesso, ProcedimentoPadrao
from setup.serializers import (
    EtapaProcessoSerializer,
    # SetupSerializer,
    OrdemProcessoSerializer,
    ProcedimentoShortSerializer, ProcedimentoDetailsSerializer, ProcedimentoStatusSerializer,
    RelatorioPeriodoSerializar, ProcedimentoSerializer)


class OrdemProcessoViewSet(ModelViewSet):
    queryset = OrdemProcesso.objects.all()
    serializer_class = OrdemProcessoSerializer


class EtapaProcessoViewSet(ModelViewSet):
    queryset = EtapaProcesso.objects.all()
    serializer_class = EtapaProcessoSerializer

    def create(self, request, *args, **kwargs):
        # op etapa gerente maquina descrica status
        data = request.data
        op = self.request.data.get('op', None)
        gerente = self.request.data.get('gerente', None)
        maquina = self.request.data.get('maquina', None)
        nivel = self.request.data.get('nivel', None)

        try:
            etapa = EtapaProcesso(etapa=data['etapa'], descricao=data['descricao'], nivel=data['nivel'], linha=data['linha'])

            etapa.op = OrdemProcesso.objects.get(id=op)
            etapa.gerente = User.objects.get(id=gerente)
            etapa.maquina = Maquinas.objects.get(id=maquina)

            etapa.save()

            procedimentoPadrao = ProcedimentoPadrao.objects.filter(nivel=nivel)

            for padrao in procedimentoPadrao:

                procedimento = Procedimento(ordem_roteiro=padrao.ordem_roteiro, descricao=padrao.descricao,
                                            tempo_estimado=padrao.tempo_estimado, tipo=padrao.tipo)

                procedimento.setor = padrao.setor
                procedimento.operador = padrao.operador
                procedimento.tempo_estimado_ms = self.convert_date_ms(padrao.tempo_estimado)
                procedimento.processo = EtapaProcesso.objects.get(id=etapa.id)

                procedimento.save()

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print (e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def convert_date_ms(self, date_string):

          date_time = datetime.strptime(date_string, '%H:%M:%S').time()

          t_hora_str = int(date_time.strftime('%H'))
          t_min_str = int(date_time.strftime('%M'))
          t_seg_str = int(date_time.strftime('%S'))

          total_ms = timedelta(hours=t_hora_str, minutes=t_min_str, seconds=t_seg_str).seconds * 1000
          return total_ms

    def update(self, request, *args, **kwargs):
        etapa = self.get_object()
        etapa.status = request.data.get('status', etapa.status)
        etapa.descricao = request.data.get('descricao', etapa.descricao)
        etapa.etapa = request.data.get('etapa', etapa.etapa)
        etapa.nivel = request.data.get('nivel', etapa.nivel)
        try:
            gerente = request.data.get('gerente', None)
            maquina = request.data.get('maquina', None)
            etapa = request.data.get('nivel', None)
            etapa.gerente = User.objects.get(id=gerente)
            etapa.maquina = Maquinas.objects.get(id=maquina)
            etapa.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    # Lista todos os processos (etapas) associadas a uma OP
    # url etapa-processo/{op_id}/listar_por_op/
    @action(methods=['get'], detail=True)
    def listar_por_op(self, request, pk):
        queryset = EtapaProcesso.objects.filter(op=pk)
        serializer = EtapaProcessoSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def etapa_ativos(self, request):
        etapas = EtapaProcesso.objects.filter(status=1)
        serializer = EtapaProcessoSerializer(etapas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CriarProcedimento(APIView):

    def post(self, request, format=None):
        print (request.data)

        file_serializer = ProcedimentoSerializer(data=request.data)

        if file_serializer.is_valid():

            objeto = file_serializer.save()

            porque_serializer = ProcedimentoSerializer(objeto)

            return Response(porque_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def create(self, request, *args, **kwargs):
        data = request.data
        print (data)
        try:
            procedimento = Procedimento(ordem_roteiro=data['ordem_roteiro'], descricao=data['descricao'],
                                        tempo_estimado=data['tempo_estimado'], tipo=data['tipo'])

            operador = User.objects.get(id=data['operador'])
            procedimento.operador = operador
            # setor_desc = data.get('setor', None)
            # procedimento.setor = setor[0]  # Cargo.objects.get(id=data['setor'])

            # procedimento.setor = Cargo.objects.filter(descricao=data['setor'])

            predecessor = self.request.data.get('predecessor', None)

            if predecessor:
                procedimento.predecessor = Procedimento.objects.get(id=predecessor)

            procedimento.processo = EtapaProcesso.objects.get(id=data['processo'])
            procedimento.tempo_estimado_ms = self.convert_date_ms(procedimento.tempo_estimado)

            try:
                procedimento.save()
            except Exception as e:
                print (e)
            print("Procedimento salvo")
            serializer = ProcedimentoShortSerializer(procedimento)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e.args[0])
            return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        print("Retrieve")
        procedimento = self.get_object()
        serializer = ProcedimentoDetailsSerializer(procedimento)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        print("Update")
        return super(ProcedimentoViewSet, self).update(request, *args, **kwargs)

    # Usar o metodo HTTP PATCH no front-end
    def partial_update(self, request, *args, **kwargs):
        print("Parcial Update")
        procedimento = self.get_object()

        # TODO Nesse trecho podem ser colocados os campos a serem atualizados quando for necessário
        procedimento.descricao = request.data.get('descricao', procedimento.descricao)
        procedimento.tempo_estimado = request.data.get('tempo_estimado', procedimento.tempo_estimado)
        procedimento.status = request.data.get('status', procedimento.status)

        try:
            operador = request.data.get('operador', None)
            if operador:
                operador_id = User.objects.get(id=operador)
                procedimento.operador = operador_id
        except Exception as e:
            return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

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
            print(e.args[0])
            return Response({'mensage': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def finalizar_procedimento(self, request, pk):
        procedimento = self.get_object()

        procedimento.hora_fim = request.data.get('hora_fim', None)
        procedimento.montador = request.data.get('montador', None)
        procedimento.status = 3

        try:
            inicio = procedimento.hora_inicio.strftime("%Y-%m-%d %H:%M:%S")
            data_inicio = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
            data_fim = datetime.strptime(procedimento.hora_fim, "%Y-%m-%d %H:%M:%S")
            result = (data_fim - data_inicio).seconds

            procedimento.tempo_realizado_ms = str(result * 1000)
            procedimento.tempo_realizado = self.convert_ms_date_mask(procedimento.tempo_realizado_ms)
            procedimento.save()
            serializer = ProcedimentoDetailsSerializer(procedimento)

            self.verificar_procedimento(procedimento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            msg = e.args[0]
            print(msg)
            return Response({'mensage': msg}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def finalizar_com_justificativa(self, request, pk):
        procedimento = self.get_object()

        procedimento.hora_fim = request.data.get('hora_fim', None)
        procedimento.status = request.data.get('status', None)
        procedimento.observacao = request.data.get('observacao', None)
        procedimento.montador = request.data.get('montador', None)

        try:
            if procedimento.status == '4':
                inicio = procedimento.hora_inicio.strftime("%Y-%m-%d %H:%M:%S")
                data_inicio = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
                data_fim = datetime.strptime(procedimento.hora_fim, "%Y-%m-%d %H:%M:%S")
                result = (data_fim - data_inicio).seconds

                procedimento.tempo_realizado_ms = str(result * 1000)
                procedimento.tempo_realizado = self.convert_ms_date_mask(procedimento.tempo_realizado_ms)

            # now = datetime.now()
            # procedimento.hora_inicio = now

            procedimento.save()
            serializer = ProcedimentoDetailsSerializer(procedimento)

            self.verificar_procedimento(procedimento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            msg = e.args[0]
            print('msg de erro ', msg)
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

                externo = queryset.filter(tipo=1).order_by('ordem_roteiro')
                interno = queryset.filter(tipo=2).order_by('ordem_roteiro')

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
            operador = User.objects.get(id=setor)
            procedimento = Procedimento.objects.filter(status=1) | Procedimento.objects.filter(status=2)

            procedimento = procedimento.values(
                'processo__id',
                'processo__descricao',
                'processo__maquina__descricao',
                'processo__op__descricao',
                'processo__etapa',
                'processo__hora_inicio',
                'processo__gerente__name',
            ).annotate(qtde_atividades=Count('setor')).filter(
                operador=operador
            )
            if op:
                procedimento = procedimento.filter(processo__op=op)

            if not procedimento:
                return Response({'message': 'List is empty or null'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'etapa_processo': procedimento}, status=status.HTTP_200_OK)
        except Exception as e:
            mensagem = {'error': e}
            return Response(mensagem, status=404)

    @action(methods=['get'], detail=False)
    def verificar_procedimento_aberto(self, request):
        user = self.request.query_params.get('operador', None)

        try:
            criterion1 = Q(status=1)
            criterion2 = Q(status=2)
            procedimento = Procedimento.objects.filter(operador=user)
            if not procedimento:  # Verifica se a lista for zero, vazio ou false
                return Response({'menssage': 'Empty List'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProcedimentoDetailsSerializer(procedimento, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'menssage': e.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False)
    def reutilizar_setup(self, request):
        etapa_id = request.data.get('etapa_id', None)

        procedimentos = Procedimento.objects.filter(processo__id=int(etapa_id))
        etapa = procedimentos[0].processo

        obj_etapa = EtapaProcesso.objects.create(
            op=etapa.op, maquina=etapa.maquina,
            descricao=etapa.descricao
        )
        query_list = list()
        for pro in procedimentos:
            obj = Procedimento.objects.create(
                ordem_roteiro=pro.ordem_roteiro, descricao=pro.descricao,
                setor=pro.setor, tempo_estimado=pro.tempo_estimado,
                tempo_estimado_ms=pro.tempo_estimado_ms, status=1,
                processo=obj_etapa, tipo=pro.tipo
            )
            query_list.append(obj)

        serializer = ProcedimentoShortSerializer(query_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_200_OK)

    def convert_date_ms(self, date_string):

        date_time = datetime.strptime(date_string, '%H:%M:%S').time()

        t_hora_str = int(date_time.strftime('%H'))
        t_min_str = int(date_time.strftime('%M'))
        t_seg_str = int(date_time.strftime('%S'))

        total_ms = timedelta(hours=t_hora_str, minutes=t_min_str, seconds=t_seg_str).seconds * 1000
        return total_ms

    def convert_ms_date_mask(self, request_ms):
        request_seconds = int(request_ms) // 1000
        out = timedelta(seconds=request_seconds)
        return str(out)


class RelatoriosViewSet(ModelViewSet):
    queryset = Procedimento.objects.all()
    serializer_class = RelatorioPeriodoSerializar

    @action(methods=['post'], detail=False)
    def processo_por_periodo(self, request):
        processo = request.data.get('processo_desc', None)
        processo_id = request.data.get('processo_id', None)
        data_inicio = request.data.get('data_inicio', None)
        data_fim = request.data.get('data_fim', None)

        queryset = ''

        try:
            data_inicio = data_inicio + ' 00:00:00'
            data_fim = data_fim + ' 23:59:59'

            date_inicio = datetime.strptime(data_inicio, "%d/%m/%Y %H:%M:%S")
            date_fim = datetime.strptime(data_fim, "%d/%m/%Y %H:%M:%S")
            if processo:
                queryset = Procedimento.objects.filter(processo__descricao=processo)

            elif processo_id:
                queryset = Procedimento.objects.filter(processo__id=processo_id)

            if queryset:

                queryset = queryset.filter(hora_inicio__range=(date_inicio, date_fim))

                externo = []
                interno = []
                for procedimento in queryset:
                    if procedimento.tipo == 1:
                        externo.append(procedimento)
                    else:
                        interno.append(procedimento)
                if queryset:

                    filtro = {
                        'procedimento': '',  # queryset[0].processo.descricao,
                        'data_inicio': data_inicio,
                        'data_fim': data_fim}

                    serializer_externo = RelatorioPeriodoSerializar(externo, many=True)
                    serializer_interno = RelatorioPeriodoSerializar(interno, many=True)

                    data = {
                        'filtro': filtro,
                        'setup_externo': serializer_externo.data,
                        'setup_interno': serializer_interno.data
                    }
                else:
                    data = {'mensagem': 'Nenhum dado encontrado'}
                return Response(data, status=status.HTTP_200_OK)
            else:
                msg = 'Dados informados não encontrados'
                print(msg, 'queryset >> ', queryset)
                return Response({'mensagem': msg}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print('error > ', e.args[0])
            return Response({'mensagem': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
