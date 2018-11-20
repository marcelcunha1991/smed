from django.contrib import admin
from setup.models import Setup, Procedimento, Processo


class SetupAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'processo', 'area_responsavel', 'tipo', 'status']


class ProcessoAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'descricao', 'gerente', 'maquina', 'status']


class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'setup', 'operador', 'data_inicio', 'data_fim', 'status']


admin.site.register(Setup, SetupAdmin)
admin.site.register(Processo, ProcessoAdmin)
admin.site.register(Procedimento, ProcedimentoAdmin)
