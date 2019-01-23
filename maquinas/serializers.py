from rest_framework.serializers import ModelSerializer

from maquinas.models import Tipo, Maquinas


class TipoSerializer(ModelSerializer):
    class Meta:
        model = Tipo
        fields = '__all__'


class MaquinasSerializer(ModelSerializer):

    class Meta:
        model = Maquinas
        fields = ('id', 'descricao', 'tipo', 'tipo_nome', 'status')
