from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50, choices=[('Vendedor', 'Vendedor'), ('Gerente', 'Gerente')])
    login = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)  # Use um campo adequado para armazenar senhas de forma segura

    def __str__(self):
        return self.nome

class Vendedor(models.Model):
    id = models.AutoField(primary_key=True)
    funcionario = models.OneToOneField(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return self.funcionario.nome

class Administrador(models.Model):
    id = models.AutoField(primary_key=True)
    funcionario = models.OneToOneField(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return self.funcionario.nome

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome

class VeiculoEstoque(models.Model):
    id = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    numero_de_chassi = models.CharField(max_length=17, unique=True)
    data_de_entrada = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano})"

class CarroEncomenda(models.Model):
    id = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30)
    preco_sugerido = models.DecimalField(max_digits=10, decimal_places=2)
    descricao_opcionais = models.TextField(blank=True, null=True)
    prazo_entrega_estimado = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} (Encomenda - {self.ano})"

class Venda(models.Model):
    id = models.AutoField(primary_key=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo_estoque = models.ForeignKey(VeiculoEstoque, on_delete=models.SET_NULL, null=True, blank=True)
    carro_encomenda = models.ForeignKey(CarroEncomenda, on_delete=models.SET_NULL, null=True, blank=True)
    data_da_venda = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    tipo_veiculo = models.CharField(max_length=10, choices=[('Estoque', 'Estoque'), ('Encomenda', 'Encomenda')])
    status_venda = models.CharField(max_length=20)

    def __str__(self):
        return f"Venda #{self.id} em {self.data_da_venda.strftime('%d/%m/%Y %H:%M')}"

class Pagamento(models.Model):
    id = models.AutoField(primary_key=True)
    venda = models.OneToOneField(Venda, on_delete=models.CASCADE)
    meio_pagamento = models.CharField(max_length=50)
    status_pagamento = models.CharField(max_length=20)

    def __str__(self):
        return f"Pagamento #{self.id} da Venda #{self.venda.id}"

class CartaoCredito(models.Model):
    pagamento = models.OneToOneField(Pagamento, on_delete=models.CASCADE)
    numero_cartao = models.CharField(max_length=20)
    validade = models.DateField()
    codigo_seguranca = models.CharField(max_length=4)
    nome_impresso = models.CharField(max_length=100)

    def __str__(self):
        return f"Cartão de Crédito ****-****-****-{self.numero_cartao[-4:]}"

class ContratoVenda(Venda):
    # A classe ContratoVenda herda todos os campos de Venda
    pass

    def __str__(self):
        return f"Contrato de Venda #{self.id} em {self.data_da_venda.strftime('%d/%m/%Y %H:%M')}"