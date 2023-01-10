from django.db import models
from perfil.models import Perfil
from abc import ABC, abstractmethod

# Create your models here.

class IFatorDeConsumoDeAgua(ABC):

    @abstractmethod
    def calcular(perfil: Perfil) -> float:
        pass


class FatorDeConsumoPeso(IFatorDeConsumoDeAgua):
    def __init__(self) -> None:
        self.indice = 35

    def calcular(self, perfil: Perfil) -> float:
        return self.indice * perfil.peso

class FatorDeConsumoTeste(IFatorDeConsumoDeAgua):
    def __init__(self) -> None:
        self.indice = 0.1

    def calcular(self, perfil: Perfil) -> float:
        return self.indice * perfil.peso

class FatorDeConsumoADM:

    FATORES_DE_CONSUMO = []

    def registrar(fator_de_consumo : IFatorDeConsumoDeAgua):
        FatorDeConsumoADM.FATORES_DE_CONSUMO.append(fator_de_consumo)


class GuiaDeHidratacaoPessoal(models.Model):
    recomendacao = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    meta = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def calcular_recomendacao(self, perfil):
        total = 0
        for fator_de_consumo in FatorDeConsumoADM.FATORES_DE_CONSUMO:
            fator = fator_de_consumo()
            total += fator.calcular(perfil)

        return total