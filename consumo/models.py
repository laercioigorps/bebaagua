from django.db import models
from perfil.models import Perfil

# Create your models here.

class ConsumoDia(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    is_meta_atingida = models.BooleanField(default=False)
    consumo = models.DecimalField(max_digits=6, decimal_places=2)

class Consumo(models.Model):
    consumoDia = models.ForeignKey(ConsumoDia, on_delete=models.CASCADE, related_name="consumos", null=True)
    volume = models.DecimalField(max_digits=6, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)