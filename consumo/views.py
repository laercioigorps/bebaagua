from django.shortcuts import render
from rest_framework.views import APIView
from .models import Copo
from rest_framework import serializers
from rest_framework.response import Response
# Create your views here.

class ListarCoposView(APIView):

    class CopoSerializer(serializers.ModelSerializer):
        class Meta:
            model = Copo
            fields = ['nome']


    def get(self, request):
        copos = Copo.objects.all()
        serializer = self.CopoSerializer(copos, many=True)
        return Response(data=serializer.data)