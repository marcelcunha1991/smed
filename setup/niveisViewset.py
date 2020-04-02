from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from setup.models import Niveis
from setup.serializers import NivelSerializer


class CriarNivel(APIView):


  def post(self, request, format=None):

      file_serializer = NivelSerializer(data=request.data)

      if file_serializer.is_valid():

          objeto = file_serializer.save()

          porque_serializer = NivelSerializer(objeto)

          return Response(porque_serializer.data, status=status.HTTP_200_OK)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalheNiveis(APIView):

    def post(self,request,format=None):

        nivel_id = request.POST.get("id")

        try:
            if(nivel_id is not None):
                nivel = Niveis.objects.get(id=nivel_id)
                nivel_serializer = NivelSerializer(nivel)
                response = {'niveis': nivel_serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            else:
                nivel = Niveis.objects.all().order_by('-id')
                nivel_serializer = NivelSerializer(nivel, many=True)
                response = {'niveis': nivel_serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        except Exception as e:

            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveNivel(APIView):

    def post(self, request, format=None):

        nivel_id = request.POST.get("id")

        try:
            if nivel_id is not None:
                Niveis.objects.filter(id=nivel_id).delete()
            else:
                Niveis.objects.all().delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)



class AlteraNivel(APIView):

    def post(self, request, format=None):

        nivel_id = request.POST.get("id")

        niveis = Niveis.objects.get(id=nivel_id)

        for attr, value in request.data.items():
            if value:
                setattr(niveis, attr, value)
        niveis.save()

        return Response(status=status.HTTP_200_OK)