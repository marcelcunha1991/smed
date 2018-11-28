from rest_framework.serializers import ModelSerializer

from setup.models import EtapaProcesso, Setup, Procedimento, OrdemProcesso


class OrdemProcessoSerializer(ModelSerializer):
    class Meta:
        model = OrdemProcesso
        fields = '__all__'


class EtapaProcessoSerializer(ModelSerializer):
    op = OrdemProcessoSerializer()

    class Meta:
        model = EtapaProcesso
        fields = ('id', 'op', 'etapa', 'gerente_desc', 'maquina', 'descricao', 'status')


class SetupSerializer(ModelSerializer):

    class Meta:
        model = Setup
        fields = '__all__'


class ProcedimentoSerializer(ModelSerializer):
    class Meta:
        model = Procedimento
        fields = '__all__'
