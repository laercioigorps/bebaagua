from django.shortcuts import render
from rest_framework.views import APIView
from .models import Copo, ConsumoDia, Consumo
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
import datetime
# Create your views here.

class ListarCoposView(APIView):

    class CopoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Copo
            fields = '__all__'


    def get(self, request):
        copos = Copo.objects.all()
        serializer = self.CopoSerializer(copos, many=True)
        return Response(data=serializer.data)

class RegistrarConsumoCopoView(APIView):

    def post(self, request, username):
        try:
            user = get_user_model().objects.get(username=username)
            copo = Copo.objects.get(pk=int(request.data.get("copo")))
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        consumosDia = ConsumoDia.objects.filter(perfil=user.perfil).filter(data__range=(today_min, today_max))
        if(consumosDia.exists()):
            consumoDia = consumosDia.first()
        else:
            consumoDia = ConsumoDia.objects.create(perfil=user.perfil, consumo=0)
        consumo = Consumo.objects.create(volume=copo.volume, consumoDia = consumoDia)
        return Response(status=status.HTTP_201_CREATED, data={
            "id": consumo.id,
            "volume" : consumo.volume,
        })