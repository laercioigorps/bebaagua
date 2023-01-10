from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Perfil
from rest_framework.serializers import ModelSerializer
from rest_framework import status

# Create your views here.

class CriarPerfilView(APIView):

    class PerfilSerializer(ModelSerializer):
        class Meta:
            model = Perfil
            fields = ["peso"]


    def post(self, request):
        perfilSerializer = self.PerfilSerializer(data=request.data)
        if(perfilSerializer.is_valid()):
            perfil = perfilSerializer.save()
            try:
                usuario = get_user_model().objects.create_user(
                    username=request.data["username"], 
                    nome=request.data["nome"],
                    perfil = perfil
                )
            except Exception:
                perfil.delete()
                return Response(status=status.HTTP_400_BAD_REQUEST) 
        else:
            print(perfilSerializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "username": usuario.username,
                "nome" : usuario.nome,
                "perfil": perfilSerializer.data
            },
        )
