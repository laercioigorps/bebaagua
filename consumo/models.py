from django.db import models
from perfil.models import Perfil

# Create your models here.

class ConsumoDia(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    data = models.DateField()
    is_meta_atingida = models.BooleanField(default=False)
    consumo = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.data.strftime("%Y-%m-%d")

class Consumo(models.Model):
    consumoDia = models.ForeignKey(ConsumoDia, on_delete=models.CASCADE, related_name="consumos", null=True)
    volume = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)