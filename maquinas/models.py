from django.db import models


class Tipo(models.Model):
    nome = models.CharField(max_length=45)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipo de Maquina'
        verbose_name_plural = 'Tipos de Maquinas'


class Maquinas(models.Model):
    descricao = models.CharField(max_length=45)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Maquina'
        verbose_name_plural = 'Maquinas'
