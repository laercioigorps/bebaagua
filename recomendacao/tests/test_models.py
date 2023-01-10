import pytest
from perfil.models import Perfil
from ..models import FatorDeConsumoPeso

def test_fator_de_consumo_de_agua_peso():
    perfil = Perfil(peso=75)
    fator_de_consumo = FatorDeConsumoPeso()
    assert hasattr(fator_de_consumo, "indice")
    #este indice indica que o calculo de consumo de água recomendado é de 0.35ml/kg.
    fator_de_consumo.indice = 0.35
    assert fator_de_consumo.calcular(perfil) == 26.25