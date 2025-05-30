from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class VeiculoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class Veiculo(models.Model):
    marca = models.CharField(max_length=100, verbose_name="Marca")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    ano_fabricacao = models.IntegerField(verbose_name="Ano de Fabricação")
    ano_modelo = models.IntegerField(verbose_name="Ano do Modelo", null=True, blank=True)
    placa = models.CharField(max_length=8, unique=True, verbose_name="Placa", help_text="Formato AAA-9999 ou ABC1D23")
    chassi = models.CharField(max_length=17, unique=True, verbose_name="Chassi")
    cor = models.CharField(max_length=50, verbose_name="Cor")
    preco_compra = models.DecimalField(
        max_digits=15,  
        decimal_places=2,
        verbose_name="Preço de Compra",
        null=True, 
        blank=True
    )
    preco_venda_sugerido = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        verbose_name="Preço de Venda Sugerido"
    )
    data_entrada = models.DateField(default=timezone.now, verbose_name="Data de Entrada no Estoque")

    DISPONIVEL = 'disponivel'
    EM_NEGOCIACAO = 'em_negociacao'
    VENDIDO = 'vendido'
    STATUS_CHOICES = [
        (DISPONIVEL, 'Disponível'),
        (EM_NEGOCIACAO, 'Em Negociação'),
        (VENDIDO, 'Vendido'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DISPONIVEL,
        verbose_name="Status"
    )
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
    
    deleted = models.BooleanField(default=False, verbose_name="Excluído")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de Exclusão")
    
    objects = VeiculoManager() 
    all_objects = models.Manager() 
    
    def soft_delete(self):
        if self.venda_set.exists():
            raise ValidationError("Não é possível excluir um veículo vinculado a vendas")
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted', 'deleted_at'])
        
        if self.status != self.VENDIDO:
            self.status = self.VENDIDO
            self.save(update_fields=['status'])

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa or 'Sem Placa'}) - {self.status}"

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['-data_entrada', 'marca', 'modelo']