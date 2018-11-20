from rest_framework.serializers import ModelSerializer

from setup.models import Processo, Setup, Procedimento


class ProcessoSerializer(ModelSerializer):
    class Meta:
        model = Processo
        fields = '__all__'


class SetupSerializer(ModelSerializer):
    class Meta:
        model = Setup
        fields = '__all__'


class ProcedimentoSerializer(ModelSerializer):
    class Meta:
        model = Procedimento
        fields = '__all__'
