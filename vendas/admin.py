from django.contrib import admin
from .models import Venda

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = (
        'cliente', 
        'veiculo', 
        'valor', 
        'data_venda', 
        'forma_pagamento',
        'deleted', 
        'deleted_at'
    )
    list_filter = ('forma_pagamento', 'deleted', 'data_venda')
    search_fields = ('cliente__nome', 'veiculo__modelo')
    readonly_fields = ('deleted', 'deleted_at')
    date_hierarchy = 'data_venda'
    
    fieldsets = (
        ('Informações da Venda', {
            'fields': (
                'cliente', 
                'veiculo', 
                'valor',
                'data_venda',
                'forma_pagamento',
                'observacoes'
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