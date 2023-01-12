from django.shortcuts import render
from rest_framework.views import APIView
from .models import Copo, ConsumoDia, Consumo
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
import datetime
# Create your views here.

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

        if(serializer.is_valid()):
            consumosDia = ConsumoDia.objects.filter(perfil=user.perfil).filter(data__range=(hoje_min, hoje_max))
            if(consumosDia.exists()):
                consumoDia = consumosDia.first()
            else:
                consumoDia = ConsumoDia.objects.create(perfil=user.perfil, consumo=0)
            
            consumo = Consumo.objects.create(volume=serializer.validated_data["volume"], consumoDia = consumoDia)
            consumoDia.consumo += serializer.validated_data["volume"]
            if(consumoDia.consumo >= user.perfil.meta):
                consumoDia.is_meta_atingida = True
            consumoDia.save()

            return Response(status=status.HTTP_201_CREATED, data={
                "id": consumo.id,
                "volume" : consumo.volume,
            })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        