from django.shortcuts import render
from rest_framework.views import APIView
from .models import ConsumoDia, Consumo, Perfil
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
import datetime

# Create your views here.


def get_perfil(username):
    try:
        perfil = Perfil.objects.get(username=username)
    except Exception:
        perfil = None
    return perfil


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ["username", "nome", "peso", "meta"]


class ConsumoSerializer(serializers.Serializer):
        volume = serializers.IntegerField()


class CriarPerfilView(APIView):
    def post(self, request):
        perfilSerializer = PerfilSerializer(data=request.data)
        if perfilSerializer.is_valid():
            try:
                perfil = perfilSerializer.save()
            except Exception:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"erro": "usuário inválido"},
                )
            perfil.meta = perfil.calcular_meta()
            perfil.save()

            return Response(status=status.HTTP_201_CREATED, data=perfilSerializer.data)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=perfilSerializer.errors
            )


class ListarPerfisView(APIView):
    def get(self, request):
        perfis = Perfil.objects.all()
        serializer = PerfilSerializer(perfis, many=True)
        return Response(data=serializer.data)


class DetalhePerfilView(APIView):
    def get(self, request, username):
        perfil = get_perfil(username)
        if not perfil:
            return Response("Usuário invalido", status=status.HTTP_400_BAD_REQUEST)
        serializer = PerfilSerializer(perfil)
        return Response(serializer.data)

    def put(self, request, username):
        perfil = get_perfil(username)
        if not perfil:
            return Response("Usuário invalido", status=status.HTTP_400_BAD_REQUEST)
        perfilSerializer = PerfilSerializer(perfil, data=request.data, partial=True)
        if perfilSerializer.is_valid():
            perfil = perfilSerializer.save()
            if "meta" not in perfilSerializer.validated_data:
                perfil.meta = perfil.calcular_meta()
                perfil.save()
            return Response(data=perfilSerializer.data)
        else:
            return Response(
                data=perfilSerializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class RegistrarConsumoView(APIView):
    

    def post(self, request, username):
        perfil = get_perfil(username)
        if not perfil:
            return Response("Usuário invalido", status=status.HTTP_400_BAD_REQUEST)
        serializer = ConsumoSerializer(data=request.data)
        hoje_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        hoje_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

        if serializer.is_valid():
            consumosDia = ConsumoDia.objects.filter(perfil=perfil).filter(
                data__range=(hoje_min, hoje_max)
            )
            if consumosDia.exists():
                consumoDia = consumosDia.first()
            else:
                consumoDia = ConsumoDia.objects.create(
                    perfil=perfil, consumo=0, data=datetime.date.today()
                )

            consumo = Consumo.objects.create(
                volume=serializer.validated_data["volume"], consumoDia=consumoDia
            )
            consumoDia.consumo += serializer.validated_data["volume"]
            if consumoDia.consumo >= perfil.meta:
                consumoDia.is_meta_atingida = True
            consumoDia.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    "id": consumo.id,
                    "volume": consumo.volume,
                },
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class ResumoConsumoView(APIView):

    def get(self, request, username, data=None):
        perfil = get_perfil(username)
        if not perfil:
            return Response("Usuário invalido", status=status.HTTP_400_BAD_REQUEST)
        if data:
            try:
                data = datetime.datetime.strptime(data, "%Y-%m-%d").date()
            except:
                return Response("formato de data inválido", status=status.HTTP_400_BAD_REQUEST)
        else:
            data = datetime.date.today()
        consumosDia = ConsumoDia.objects.filter(perfil=perfil).filter(
            data__year=data.year, data__month=data.month, data__day=data.day
        )
        if consumosDia.exists():
            consumoDia = consumosDia.first()
            consumo_restante = perfil.meta - consumoDia.consumo
            if consumo_restante < 0:
                consumo_restante = 0

            porcentagem_consumida_da_meta = consumoDia.consumo / perfil.meta * 100
            if porcentagem_consumida_da_meta > 100:
                porcentagem_consumida_da_meta = 100
            return Response(
                data={
                    "meta": perfil.meta,
                    "consumo": consumoDia.consumo,
                    "consumo_restante": consumo_restante,
                    "porcentagem_consumida_da_meta": round(
                        porcentagem_consumida_da_meta, 2
                    ),
                    "meta_atingida": consumoDia.is_meta_atingida,
                    "data" : consumoDia.data.strftime("%d/%m/%Y")
                },
            )
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
