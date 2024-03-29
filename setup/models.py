
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
    nivel = models.IntegerField(blank=True, null=True)
    maquina = models.ForeignKey(Maquinas, on_delete=models.DO_NOTHING, blank=True, null=True)
    descricao = models.CharField(max_length=100, blank=True, null=True)
    gerente = models.ForeignKey(User, verbose_name='Gerente', on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, blank=True, null=True)
    codigo = models.CharField(max_length=100, blank=True, null=True)
    hora_inicio = models.DateTimeField(blank=True, null=True)
    opc = models.CharField(max_length=20,null=True)
    linha = models.CharField(max_length=20, blank=True, null=True)
    hora_programada = models.CharField(max_length=10, blank=True, null=True)
    quantidadeKit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '%s - %s - Etapa: %s ' % (self.op, self.descricao, self.etapa)

    class Meta:
        verbose_name = 'Etapa do Processo'
        verbose_name_plural = 'Etapas do Processo'
        unique_together = (('op', 'etapa'),)

    @property
    def gerente_name(self):
        return '%s' % self.gerente.name or self.gerente.username

    @property
    def op_descricao(self):
        return '%s' % self.op.descricao

    @property
    def maquina_descricao(self):
        return '%s' % self.maquina.descricao


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
    descricao = models.CharField(max_length=400, blank=True, null=True)
    setor = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING, blank=True, null=True)
    predecessor = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    operador = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Operador', on_delete=models.DO_NOTHING,
                                 blank=True, null=True)  # usuario logado no app
    montador = models.CharField(max_length=50, blank=True, null=True)
    tempo_estimado = models.CharField(max_length=10, blank=True, null=True)
    tempo_estimado_ms = models.CharField(max_length=50, blank=True, null=True)
    tempo_realizado = models.CharField(max_length=10, blank=True, null=True)
    tempo_realizado_ms = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, blank=True, null=True)
    observacao = models.TextField(max_length=100, blank=True, null=True)
    processo = models.ForeignKey(EtapaProcesso, verbose_name='Etapa', on_delete=models.DO_NOTHING, blank=True, null=True)
    tipo = models.IntegerField(choices=TIPO_CHOICES, null=True, blank=True)
    hora_inicio = models.DateTimeField(blank=True, null=True)
    hora_fim = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.descricao, self.ordem_roteiro)
        # return str(self.id)

    class Meta:
        verbose_name = 'Procedimento - Atividade'
        verbose_name_plural = 'Procedimentos - Atividades'
        unique_together = (('processo', 'ordem_roteiro', 'tipo'),)
        # ordering = ['ordem_roteiro']

    @property
    def operador_name(self):
        return '%s' % self.operador.name or self.operador.username

    @property
    def processo_descricao(self):
        return '%s' % str(self.processo.descricao)

    @property
    def predecessor_descricao(self):
        return '%s' % str(self.predecessor.descricao)

    @property
    def maquina(self):
        return '%s' % str(self.processo.maquina.descricao)

    @property
    def op(self):
        return '%s' % str(self.processo.op.descricao)


class Niveis(models.Model):
    descricao = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=True)

class ProcedimentoPadrao(models.Model):
    TIPO_CHOICES = (
        (1, 'Externo'),
        (2, 'Interno'),
    )

    nivel = models.ForeignKey(Niveis,on_delete=models.DO_NOTHING,null=True)
    ordem_roteiro = models.IntegerField(blank=True, null=True)
    descricao = models.CharField(max_length=45, blank=True, null=True)
    setor = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING, blank=True, null=True)
    operador = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='colaborador', on_delete=models.DO_NOTHING,
                                 blank=True, null=True)  # usuario logado no app
    tipo = models.IntegerField(choices=TIPO_CHOICES, null=True, blank=True)
    tempo_estimado = models.CharField(max_length=10, blank=True, null=True)
    tempo_estimado_ms = models.CharField(max_length=50, blank=True, null=True)






