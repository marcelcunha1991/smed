from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Cargo, User
from setup.models import Niveis, ProcedimentoPadrao
from setup.serializers import ProcedimentoPadraoSerializer


class CriarProcedimentoPadrao(APIView):

  def post(self, request, format=None):

      niveis = Niveis.objects.get(id= request.data['nivel'])
      setor = Cargo.objects.get(id=request.data['setor'])
      operador = User.objects.get(id=request.data['operador']['id'])

      file_serializer = ProcedimentoPadraoSerializer(data=request.data)

      if file_serializer.is_valid():


          file_serializer.validated_data['nivel'] = niveis
          file_serializer.validated_data['setor'] = setor
          file_serializer.validated_data['operador'] = operador

          objeto = file_serializer.save()

          porque_serializer = ProcedimentoPadraoSerializer(objeto)

          return Response(porque_serializer.data, status=status.HTTP_200_OK)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DetalheProcedimentoPadrao(APIView):

    def post(self,request,format=None):

        nivel_id = request.POST.get("id")

        try:
            if(nivel_id is not None):
                nivel = ProcedimentoPadrao.objects.get(id=nivel_id)
                nivel_serializer = ProcedimentoPadraoSerializer(nivel)
                response = {'procedimentoPadrao': nivel_serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            else:
                nivel = ProcedimentoPadrao.objects.all().order_by('-id')
                nivel_serializer = ProcedimentoPadraoSerializer(nivel, many=True)
                response = {'procedimentoPadrao': nivel_serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        except Exception as e:

            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveProcedimentoPadrao(APIView):

    def delete(self, request, padrao_id):

        try:
            if padrao_id is not None:
                ProcedimentoPadrao.objects.filter(id=padrao_id).delete()
            else:
                ProcedimentoPadrao.objects.all().delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)



class AlteraProcedimentoPadrao(APIView):

    def post(self, request, format=None):

        nivel_id = request.POST.get("id")

        niveis = ProcedimentoPadrao.objects.get(id=nivel_id)

        for attr, value in request.data.items():
            if value:
                setattr(niveis, attr, value)
        niveis.save()

        return Response(status=status.HTTP_200_OK)