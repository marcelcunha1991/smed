import re

from django.core import validators
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class Cargo(models.Model):
    descricao = models.CharField(max_length=35)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        'Apelido / Usuário', max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-/_ .'
                , 'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
    )
    name = models.CharField('Nome', max_length=100, blank=True)
    email = models.EmailField('E-mail', unique=True, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, blank=True, null=True)
    phone = models.CharField('Telefone', max_length=30, null=True, blank=True)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        # return self.name or self.username
        return '%s - %s' % (self.username or self.name, self.cargo)

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(" ")[0]
