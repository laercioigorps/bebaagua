from django.contrib import admin
from .models import FatorDeConsumoADM
from .models import FatorDeConsumoPeso, FatorDeConsumoTeste

# Register your models here.
FatorDeConsumoADM.registrar(FatorDeConsumoPeso)