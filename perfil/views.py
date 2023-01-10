from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Perfil
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from recomendacao.models import GuiaDeHidratacaoPessoal

# Create your views here.


class CriarPerfilView(APIView):
    class PerfilSerializer(ModelSerializer):
        class Meta:
            model = Perfil
            fields = ["peso"]

    def post(self, request):
        perfilSerializer = self.PerfilSerializer(data=request.data)
        guia = GuiaDeHidratacaoPessoal.objects.create()
        if perfilSerializer.is_valid():
            perfil = perfilSerializer.save(guia=guia)
            recomendacao = guia.calcular_recomendacao(perfil)
            perfil.guia.recomendacao = recomendacao
            perfil.guia.meta = recomendacao
            guia.save()
            try:
                usuario = get_user_model().objects.create_user(
                    username=request.data["username"],
                    nome=request.data["nome"],
                    perfil=perfil,
                )
            except Exception:
                perfil.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "username": usuario.username,
                "nome": usuario.nome,
                "perfil": perfilSerializer.data,
            },
        )


class ListarPerfisView(APIView):
    class UserSerializer(ModelSerializer):
        class PerfilSerializer(ModelSerializer):
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
    class UserSerializer(ModelSerializer):
        class PerfilSerializer(ModelSerializer):
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
        userSerializer = self.UserSerializer(user)
        perfilSerializer = self.UserSerializer.PerfilSerializer(
            user.perfil, data=request.data
        )
        if perfilSerializer.is_valid():
            perfil = perfilSerializer.save()
            return Response(userSerializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
