from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from accounts.models import User, Cargo
from accounts.serializers import UserSerializer, CargoSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginViewSet(APIView):

    def post(self, request):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                serializer = UserSerializer(user)
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

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                user.is_logged = False
                user.save()
                return Response('Deslogado', status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CargoViewSet(ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


def index(request):
    return render(request, 'index.html')
