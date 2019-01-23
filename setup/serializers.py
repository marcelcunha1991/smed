from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accounts.serializers import UserLoggedSerializer
from setup.models import EtapaProcesso, Procedimento, OrdemProcesso


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
            'id', 'ordem_roteiro', 'descricao', 'tempo_estimado', 'tempo_realizado',
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
            'id', 'ordem_roteiro', 'descricao', 'status', 'tempo_estimado', 'tempo_realizado', 'operador',
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
