from django.db import models

# Create your models here.
class Copo(models.Model):
    nome = models.CharField(max_length=70)
    volume = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return self.nome