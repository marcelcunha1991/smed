from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accounts.serializers import UserLoggedSerializer
from setup.models import EtapaProcesso, Procedimento, OrdemProcesso
from datetime import date, datetime, timedelta, time


class OrdemProcessoSerializer(ModelSerializer):
    class Meta:
        model = OrdemProcesso
        fields = '__all__'


class EtapaProcessoSerializer(ModelSerializer):
    # op = OrdemProcessoSerializer()
    status = SerializerMethodField()

    # gerente = SerializerMethodField()

    class Meta:
        model = EtapaProcesso
        fields = (
            'id', 'op', 'op_descricao', 'etapa', 'gerente', 'gerente_name',
            'maquina', 'maquina_descricao', 'descricao', 'status'
        )

    def get_status(self, obj):
        return obj.get_status_display()


#  Mostra os campos necessários quando for listar uma coleção de procedimentos
class ProcedimentoShortSerializer(ModelSerializer):
    status = SerializerMethodField()
    tipo = SerializerMethodField()

    class Meta:
        model = Procedimento
        fields = (
            'id', 'ordem_roteiro', 'descricao', 'tempo_estimado', 'tempo_estimado_ms',
            'tempo_realizado', 'tempo_realizado_ms',
            'tipo', 'hora_inicio', 'status', 'operador',
            'operador_name', 'processo', 'processo_descricao'
        )

    def get_status(self, obj):
        return obj.get_status_display()

    def get_tipo(self, obj):
        return obj.get_tipo_display()


class ProcedimentoDetailsSerializer(ModelSerializer):
    status = SerializerMethodField()
    tipo = SerializerMethodField()

    class Meta:
        model = Procedimento
        fields = (
            'id', 'ordem_roteiro', 'descricao', 'status', 'tempo_estimado', 'tempo_estimado_ms',
            'tempo_realizado', 'tempo_realizado_ms', 'operador',
            'operador_name', 'processo', 'processo_descricao', 'observacao', 'tipo',
            'hora_inicio', 'hora_fim'

        )

    def get_status(self, obj):
        return obj.get_status_display()

    def get_tipo(self, obj):
        return obj.get_tipo_display()


class ProcedimentoStatusSerializer(ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model = Procedimento
        fields = ('status',)

    def get_status(self, obj):
        return obj.get_status_display()


class RelatorioPeriodoSerializar(ModelSerializer):
    status = SerializerMethodField()
    tipo = SerializerMethodField()
    data_inicio = SerializerMethodField()
    data_final = SerializerMethodField()

    class Meta:
        model = Procedimento
        fields = ('id', 'maquina', 'op', 'descricao', 'ordem_roteiro',
                  'status', 'tempo_estimado', 'data_inicio', 'data_final',
                  'tempo_realizado', 'operador_name',
                  'processo_descricao', 'tipo', 'observacao'
                  )

    def get_status(self, obj):
        return obj.get_status_display()

    def get_tipo(self, obj):
        return obj.get_tipo_display()

    def get_data_inicio(self, obj):
        out = obj.hora_inicio
        if out:
            out = obj.hora_inicio.strftime('%d/%m/%Y %H:%M:%S')
        return out

    def get_data_final(self, obj):
        out = obj.hora_fim
        if out:
            out = obj.hora_fim.strftime('%d/%m/%Y %H:%M:%S')
        return out


class RelatorioFilterSerializer(ModelSerializer):
    class Meta:
        model = Procedimento
        fields = ('processo', 'processo_descricao', 'hora_inicio', 'hora_fim')
