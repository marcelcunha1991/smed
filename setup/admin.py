from django.contrib import admin
from setup.models import Procedimento, EtapaProcesso, OrdemProcesso


class OrdemProcessoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao']


class EtapaProcessoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'etapa', 'op', 'maquina', 'gerente', 'hora_inicio', 'status']
    list_filter = ('op',)


class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'ordem_roteiro', 'tipo', 'setor', 'operador', 'status',
                    'processo', 'hora_inicio', 'observacao']
    list_filter = ('setor', 'processo', 'tipo',)


admin.site.register(OrdemProcesso, OrdemProcessoAdmin)
# admin.site.register(Setup, SetupAdmin)
admin.site.register(EtapaProcesso, EtapaProcessoAdmin)
admin.site.register(Procedimento, ProcedimentoAdmin)
