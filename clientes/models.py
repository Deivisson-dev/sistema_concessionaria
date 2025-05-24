from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class ClienteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class Cliente(models.Model):
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve conter 11 dígitos')]
    )
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    endereco = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = ClienteManager()
    all_objects = models.Manager() 
    
    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted', 'deleted_at'])

    def __str__(self):
        return f"{self.nome} ({self.cpf})"