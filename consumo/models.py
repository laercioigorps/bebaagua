from django.db import models


class Perfil(models.Model):
    username = models.CharField(unique=True, max_length=50)
    nome = models.CharField(max_length=50)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    meta = models.PositiveIntegerField(default=0)

    def calcular_meta(self):
        return 35 * self.peso


class ConsumoDia(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    data = models.DateField()
    meta = models.PositiveIntegerField(default=0)
    meta_atingida = models.BooleanField(default=False)
    consumo = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.data.strftime('%Y-%m-%d')} - {self.consumo}"

    @property
    def consumo_restante(self):
        restante = self.meta - self.consumo
        if restante < 0:
            restante = 0
        return restante

    @property
    def porcentagem_consumida_da_meta(self):
        porcentagem = self.consumo / self.meta * 100
        if porcentagem > 100:
            porcentagem = 100
        return porcentagem


class Consumo(models.Model):
    consumoDia = models.ForeignKey(
        ConsumoDia, on_delete=models.CASCADE, related_name="consumos", null=True
    )
    volume = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
