from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Perfil(models.Model):
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    meta =  models.PositiveIntegerField(default=0)

    def calcular_meta(self):
        return 35 * self.peso

class User(AbstractUser):
    nome = CharField(blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, null=True)




