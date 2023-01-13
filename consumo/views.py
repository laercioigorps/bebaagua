from django.shortcuts import render
from rest_framework.views import APIView
from .models import ConsumoDia, Consumo, Perfil
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
import datetime

# Create your views here.


class CriarPerfilView(APIView):
    class PerfilSerializer(serializers.ModelSerializer):
        class Meta:
            model = Perfil
            fields = ["peso"]

    def post(self, request):
        perfilSerializer = self.PerfilSerializer(data=request.data)
        if perfilSerializer.is_valid():

            try:
                usuario = get_user_model().objects.create_user(
                    username=request.data["username"],
                    nome=request.data["nome"],
                )
            except Exception:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"erro": "usuário inválido"},
                )
            perfil = perfilSerializer.save()
            perfil.meta = perfil.calcular_meta()
            perfil.save()
            usuario.perfil = perfil
            usuario.save()
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=perfilSerializer.errors
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "username": usuario.username,
                "nome": usuario.nome,
                "perfil": perfilSerializer.data,
            },
        )


class ListarPerfisView(APIView):
    class UserSerializer(serializers.ModelSerializer):
        class PerfilSerializer(serializers.ModelSerializer):
            class Meta:
                model = Perfil
                fields = ["peso"]

        perfil = PerfilSerializer()

        class Meta:
            model = get_user_model()
            fields = ["username", "nome", "perfil"]

    def get(self, request):
        perfis = get_user_model().objects.all()
        serializer = self.UserSerializer(perfis, many=True)
        return Response(data=serializer.data)


class DetalhePerfilView(APIView):
    class UserSerializer(serializers.ModelSerializer):
        class PerfilSerializer(serializers.ModelSerializer):
            class Meta:
                model = Perfil
                fields = ["peso"]

        perfil = PerfilSerializer()

        class Meta:
            model = get_user_model()
            fields = ["username", "nome", "perfil"]

    def get(self, request, username):
        user = get_user_model().objects.get(username=username)
        serializer = self.UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = get_user_model().objects.get(username=username)
        if "nome" in request.data:
            user.nome = request.data.get("nome")
            user.save()
        perfilSerializer = self.UserSerializer.PerfilSerializer(
            user.perfil, data=request.data
        )
        userSerializer = self.UserSerializer(user)
        if perfilSerializer.is_valid():
            perfil = perfilSerializer.save()
            perfil.meta = perfil.calcular_meta()
            perfil.save()
            userSerializer = self.UserSerializer(user)
            return Response(userSerializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegistrarConsumoView(APIView):
    class ConsumoSerializer(serializers.Serializer):
        volume = serializers.IntegerField()

    def post(self, request, username):
        try:
            user = get_user_model().objects.get(username=username)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.ConsumoSerializer(data=request.data)
        hoje_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        hoje_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

        if serializer.is_valid():
            consumosDia = ConsumoDia.objects.filter(perfil=user.perfil).filter(
                data__range=(hoje_min, hoje_max)
            )
            if consumosDia.exists():
                consumoDia = consumosDia.first()
            else:
                consumoDia = ConsumoDia.objects.create(
                    perfil=user.perfil, consumo=0, data=datetime.date.today()
                )

            consumo = Consumo.objects.create(
                volume=serializer.validated_data["volume"], consumoDia=consumoDia
            )
            consumoDia.consumo += serializer.validated_data["volume"]
            if consumoDia.consumo >= user.perfil.meta:
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
    class ResumoInputSerializer(serializers.Serializer):
        data = serializers.DateField(
            input_formats=["%Y-%m-%d", "iso-8601"], required=False
        )

    def get(self, request, username, data=None):
        try:
            user = get_user_model().objects.get(username=username)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.ResumoInputSerializer(data=request.data)
        if data and serializer.is_valid():
            data = datetime.datetime.strptime(data, "%Y-%m-%d").date()
        else:
            data = datetime.date.today()
        print(ConsumoDia.objects.all())
        consumosDia = ConsumoDia.objects.filter(perfil=user.perfil).filter(
            data__year=data.year, data__month=data.month, data__day=data.day
        )
        if consumosDia.exists():
            consumoDia = consumosDia.first()
            consumo_restante = user.perfil.meta - consumoDia.consumo
            if consumo_restante < 0:
                consumo_restante = 0

            porcentagem_consumida_da_meta = consumoDia.consumo / user.perfil.meta * 100
            if porcentagem_consumida_da_meta > 100:
                porcentagem_consumida_da_meta = 100
            return Response(
                data={
                    "meta": user.perfil.meta,
                    "consumo": consumoDia.consumo,
                    "consumo_restante": consumo_restante,
                    "porcentagem_consumida_da_meta": round(
                        porcentagem_consumida_da_meta, 2
                    ),
                    "meta_atingida": consumoDia.is_meta_atingida,
                },
            )
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
