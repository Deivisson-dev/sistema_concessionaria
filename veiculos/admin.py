from django.contrib import admin
from .models import Veiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = (
        'marca', 
        'modelo', 
        'placa', 
        'status', 
        'deleted', 
        'deleted_at'
    )
    list_filter = ('status', 'deleted', 'marca')
    search_fields = ('marca', 'modelo', 'placa', 'chassi')
    readonly_fields = ('deleted', 'deleted_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'marca', 
                'modelo', 
                'ano_fabricacao', 
                'ano_modelo',
                'placa',
                'chassi',
                'cor'
            )
        }),
        ('Informações Financeiras', {
            'fields': (
                'preco_compra', 
                'preco_venda_sugerido'
            )
        }),
        ('Status e Observações', {
            'fields': (
                'status',
                'observacoes'
            )
        }),
        ('Datas', {
            'fields': (
                'data_entrada',
            )
        }),
        ('Soft Delete', {
            'fields': (
                'deleted',
                'deleted_at'
            ),
            'classes': ('collapse',)
        }),
    )