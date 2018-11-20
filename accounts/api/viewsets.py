from rest_framework.viewsets import ModelViewSet

from accounts.models import User, Cargo
from accounts.api.serializers import UserSerializer, CargoSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CargoViewSet(ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
