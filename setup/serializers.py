from rest_framework.serializers import ModelSerializer, SerializerMethodField

from setup.models import EtapaProcesso, Setup, Procedimento, OrdemProcesso


class OrdemProcessoSerializer(ModelSerializer):
    class Meta:
        model = OrdemProcesso
        fields = '__all__'


class EtapaProcessoSerializer(ModelSerializer):
    op = OrdemProcessoSerializer()

    # gerente = SerializerMethodField()

    class Meta:
        model = EtapaProcesso
        fields = (
            'id', 'op', 'etapa', 'gerente', 'gerente_desc',
            'maquina', 'descricao', 'status'
        )


class SetupSerializer(ModelSerializer):
    tipo = SerializerMethodField()

    class Meta:
        model = Setup
        fields = '__all__'

    def get_tipo(self, obj):
        return obj.get_tipo_display()


#  Mostra os campos necessários quando for listar uma coleção de procedimentos
class ProcedimentoShortSerializer(ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model = Procedimento
        fields = (
            'id', 'ordem_roteiro', 'tempo_estimado', 'descricao',
            'setup', 'status', 'operador'
        )

    def get_status(self, obj):
        return obj.get_status_display()


class ProcedimentoDetailsSerializer(ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model = Procedimento
        fields = '__all__'

    def get_status(self, obj):
        return obj.get_status_display()


class ProcedimentoStatusSerializer(ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model = Procedimento
        fields = ('status',)

    def get_status(self, obj):
        return obj.get_status_display()
