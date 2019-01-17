from django.conf import settings
from django.db import models

from accounts.models import Cargo, User
from maquinas.models import Maquinas


class OrdemProcesso(models.Model):
    descricao = models.CharField(max_length=45)

    def __str__(self):
        return self.descricao


# TODO colocar os campos DESCRICAO, STATUS como obrigatórios depois.
class EtapaProcesso(models.Model):
    STATUS_CHOICES = (
        (1, 'Ativo'),
        (2, 'Finalizado'),
        (3, 'Inativo'),
    )
    op = models.ForeignKey(OrdemProcesso, on_delete=models.PROTECT)
    etapa = models.IntegerField(blank=True, null=True)
    maquina = models.ForeignKey(Maquinas, on_delete=models.CASCADE, blank=True, null=True)
    descricao = models.CharField(max_length=100, blank=True, null=True)
    gerente = models.ForeignKey(User, verbose_name='Gerente', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, blank=True, null=True)
    codigo = models.CharField(max_length=100, blank=True, null=True)
    hora_inicio = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s - %s %s ' % (self.op, self.descricao, self.etapa)

    class Meta:
        verbose_name = 'Etapa do Processo'
        verbose_name_plural = 'Etapas do Processo'
        unique_together = (('op', 'etapa'),)

    @property
    def gerente_name(self):
        return '%s' % self.gerente.name or self.gerente.username


# class Setup(models.Model):
#     TIPO_CHOICES = (
#         (1, 'Externo'),
#         (2, 'Interno'),
#     )
#
#     STATUS_CHOICES = (
#         (1, 'Ativo'),
#         (2, 'Inativo'),
#     )
#
#     descricao = models.CharField(max_length=50)
#     processo = models.ForeignKey(EtapaProcesso, blank=True, null=True, on_delete=models.CASCADE,
#                                  verbose_name='Etapa do Processo')
#     responsavel = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     created = models.DateTimeField('Criado em', auto_now_add=True, blank=True, null=True)
#     # hora_inicio = models.DateTimeField(blank=True, null=True)
#     tipo = models.IntegerField(choices=TIPO_CHOICES, blank=True, null=True)
#     status = models.IntegerField(choices=STATUS_CHOICES, default=2)
#
#     def __str__(self):
#         return '%s - %s %s' % (self.processo, self.descricao, self.tipo)
#
#     class Meta:
#         unique_together = (('processo', 'tipo'),)
#
#     @property
#     def responsavel_name(self):
#         return '%s' % self.responsavel.name or self.responsavel.username


class Procedimento(models.Model):
    STATUS_CHOICES = (
        (1, 'Pendente'),
        (2, 'Realizando'),
        (3, 'Realizado com sucesso'),
        (4, 'Realizado fora do tempo'),
        (5, 'Não necessario'),
        (6, 'Finalizado com pendencias'),
    )
    TIPO_CHOICES = (
        (1, 'Externo'),
        (2, 'Interno'),
    )

    ordem_roteiro = models.IntegerField(blank=True, null=True)
    descricao = models.CharField(max_length=45, blank=True, null=True)
    # setup = models.ForeignKey(Setup, on_delete=models.CASCADE)
    setor = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null=True)
    predecessor = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    operador = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Operador', on_delete=models.CASCADE,
                                 blank=True, null=True)
    tempo_estimado = models.CharField(max_length=10, blank=True, null=True)
    tempo_realizado = models.CharField(max_length=10, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, blank=True, null=True)
    observacao = models.TextField(max_length=100, blank=True, null=True)
    processo = models.ForeignKey(EtapaProcesso, verbose_name='Etapa', on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.IntegerField(choices=TIPO_CHOICES, null=True, blank=True)
    hora_inicio = models.DateTimeField(blank=True, null=True)
    hora_fim = models.DateTimeField(blank=True, null=True)
    tempo_realizado2 = models.DurationField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.descricao, self.ordem_roteiro)
        # return str(self.id)

    class Meta:
        verbose_name = 'Procedimento - Atividade'
        verbose_name_plural = 'Procedimentos - Atividades'
        unique_together = (('processo', 'ordem_roteiro', 'tipo'),)
        # ordering = ['ordem_roteiro']
