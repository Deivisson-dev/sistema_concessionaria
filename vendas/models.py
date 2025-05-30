from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from veiculos.models import Veiculo

class FormaPagamento(models.TextChoices):
    A_VISTA = 'AV', 'À vista'
    FINANCIAMENTO = 'FN', 'Financiamento'
    PARCELADO = 'PR', 'Parcelado'

class VendaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateField()
    forma_pagamento = models.CharField(
        max_length=2,
        choices=FormaPagamento.choices,
        default=FormaPagamento.A_VISTA
    )
    observacoes = models.TextField(blank=True, null=True)
    
    deleted = models.BooleanField(default=False, verbose_name="Excluído")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de Exclusão")
    
    objects = VendaManager()  
    all_objects = models.Manager() 
    
    def __str__(self):
        return f"Venda #{self.id} - {self.veiculo} para {self.cliente}"
    
    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        
        veiculo = self.veiculo
        veiculo.status = Veiculo.DISPONIVEL
        veiculo.save(update_fields=['status'])
        
        # Salva a venda
        self.save(update_fields=['deleted', 'deleted_at'])
        
    class Meta:
        ordering = ['-data_venda']