import pytest
from perfil.models import Perfil
from ..models import FatorDeConsumoPeso, GuiaDeHidratacaoPessoal, FatorDeConsumoADM, FatorDeConsumoTeste

def test_fator_de_consumo_de_agua_peso():
    perfil = Perfil(peso=75)
    fator_de_consumo = FatorDeConsumoPeso()
    assert hasattr(fator_de_consumo, "indice")
    #este indice indica que o calculo de consumo de água recomendado é de 0.35ml/kg.
    fator_de_consumo.indice = 35
    assert fator_de_consumo.calcular(perfil) == 2625


def test_calcular_recomendacao_do_guia():
    FatorDeConsumoADM.FATORES_DE_CONSUMO = [FatorDeConsumoPeso]
    perfil = Perfil(peso=75)
    guia = GuiaDeHidratacaoPessoal()
    recomendacao = guia.calcular_recomendacao(perfil)
    assert recomendacao == 2625

def test_calcular_recomendacao_com_teste_extra():
    FatorDeConsumoADM.FATORES_DE_CONSUMO = [FatorDeConsumoPeso, FatorDeConsumoTeste]
    perfil = Perfil(peso=75)
    guia = GuiaDeHidratacaoPessoal()
    recomendacao = guia.calcular_recomendacao(perfil)
    assert recomendacao == 2632.5