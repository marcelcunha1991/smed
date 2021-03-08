from rest_framework import status
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from accounts.models import Cargo, User


class CargoSerializer(ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name', 'email', 'cargo', 'is_logged')
        # write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.password = ""
        return user


class UserLoggedSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'phone', 'cargo', 'cargo_descricao', 'is_logged')

