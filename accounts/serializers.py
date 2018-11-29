from rest_framework.serializers import ModelSerializer

from accounts.models import Cargo, User


class CargoSerializer(ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class UserSerializer(ModelSerializer):
    cargo = CargoSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'cargo', 'is_logged')
