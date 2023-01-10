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
        self.indice = 0.75

    def calcular(self, perfil: Perfil) -> float:
        return self.indice * perfil.peso