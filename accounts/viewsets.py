from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from accounts.models import User, Cargo
from accounts.serializers import UserSerializer, CargoSerializer, UserLoggedSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoggedSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserLoggedSerializer(user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = UserLoggedSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.create_user(data['username'], data['email'],
                                            data['password'])
            cargo = Cargo.objects.get(id=data['cargo'])

            user.cargo = cargo
            user.name = data['name']
            user.phone = request.data.get('phone', None)
            user.save()
            serializer = UserLoggedSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'mensage': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(APIView):

    def post(self, request):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                serializer = UserLoggedSerializer(user)
                user.is_logged = True
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'response': 'Usuário destivado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'response': 'Dados inválidos'}, status=status.HTTP_404_NOT_FOUND)


class LogoutViewSet(APIView):

    def post(self, request):
        data = request.data

        id = data.get('id', None)
        # password = data.get('password', None)

        try:
            user = User.objects.get(id=id)
            if user.is_active:
                user.is_logged = False
                user.save()
                return Response('Deslogado', status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CargoViewSet(ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


def index(request):
    return render(request, 'index.html')
