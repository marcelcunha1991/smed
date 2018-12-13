from django.contrib import admin
from setup.models import Setup, Procedimento, EtapaProcesso, OrdemProcesso


class OrdemProcessoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao']


class EtapaProcessoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'etapa', 'op', 'maquina', 'gerente', 'hora_inicio', 'status']
    list_filter = ('op',)


class SetupAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'tipo', 'processo', 'responsavel', 'created', 'status']
    list_filter = ('processo', 'status', 'tipo',)


class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'ordem_roteiro', 'setup', 'predecessor', 'setor', 'operador', 'status']
    list_filter = ('setup', 'setor',)


admin.site.register(OrdemProcesso, OrdemProcessoAdmin)
admin.site.register(Setup, SetupAdmin)
admin.site.register(EtapaProcesso, EtapaProcessoAdmin)
admin.site.register(Procedimento, ProcedimentoAdmin)
