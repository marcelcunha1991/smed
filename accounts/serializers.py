from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accounts.models import Cargo, User


class CargoSerializer(ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class UserSerializer(ModelSerializer):
    # cargo = CargoSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name', 'email', 'cargo', 'is_logged')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoggedSerializer(ModelSerializer):
    cargo = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'cargo', 'is_logged')

    def get_cargo(self, obj):
        return obj.cargo
