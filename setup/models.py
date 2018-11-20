from django.conf import settings
from django.db import models

from accounts.models import Cargo
from maquinas.models import Maquinas


# TODO colocar os campos codigo descricao como obrigatórios depois.
class Processo(models.Model):
    codigo = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.CharField(max_length=100, blank=True, null=True)
    gerente = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Gerente', on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquinas, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.descricao


class Setup(models.Model):

    TIPO_CHOICES = (
        (0, 'Outro'),
        (1, 'Externo'),
        (2, 'Interno'),
    )

    STATUS_CHOICES = (
        (0, 'Outro'),
        (1, 'Ativo'),
        (2, 'Inativo'),
    )

    descricao = models.CharField(max_length=50)
    processo = models.ForeignKey(Processo, blank=True, null=True, on_delete=models.CASCADE)
    area_responsavel = models.ForeignKey(Cargo, on_delete=models.PROTECT, blank=True, null=True)
    tempo_previsto = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    tipo = models.IntegerField(choices=TIPO_CHOICES, default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=2)

    def __str__(self):
        return self.descricao


class Procedimento(models.Model):
    setup = models.ForeignKey(Setup, on_delete=models.CASCADE)
    operador = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Operador', on_delete=models.CASCADE)
    data_inicio = models.DateTimeField(blank=True, null=True)
    data_fim = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.setup

