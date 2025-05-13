from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TIPOS = (
        ('vendedor', 'Vendedor'),
        ('gerente', 'Gerente'),
    )
    tipo = models.CharField(max_length=10, choices=TIPOS, default='vendedor')

    def __str__(self):
        return f"{self.username} ({self.tipo})"

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    id_funcionario = models.IntegerField(unique=True)
    cargo = models.CharField(max_length=50)

    def login(self):
        return "Funcionário logado no sistema."

    def visualizar_historico_compras(self):
        return "Histórico de compras visualizado."

    def consultar_cliente(self):
        return "Consulta de cliente realizada."

    def cancelar_venda(self):
        return "Venda cancelada."

    def consultar_estoque(self):
        return "Estoque consultado."

    def visualizar_vendas(self):
        return "Vendas visualizadas."

    def alterar_status_venda(self):
        return "Status da venda alterado."

    def filtrar_veiculos_por_atributo(self):
        return "Veículos filtrados por atributo."

    def consultar_veiculos(self):
        return "Veículos consultados."

    def __str__(self):
        return self.nome

class Gerente(Funcionario):
    def gerenciar_usuario_permissao(self):
        return "Usuários e permissões gerenciados."

    def cadastrar_veiculo(self):
        return "Veículo cadastrado."

    def editar_informacao_veiculo(self):
        return "Informação do veículo editada."

    def excluir_veiculo(self):
        return "Veículo excluído."

    def solicitar_compra_veiculo_montadora(self):
        return "Solicitação de compra de veículo enviada à montadora."

    def registrar_chegada_veiculo(self):
        return "Chegada de veículo registrada."

    def consolidar_pagamentos(self):
        return "Pagamentos consolidados."

    def definir_metas_faturamento(self):
        return "Metas de faturamento definidas."

    def gerar_relatorio_financeiro(self):
        return "Relatório financeiro gerado."

class Vendedor(Funcionario):
    def cadastrar_cliente(self):
        return "Cliente cadastrado."

    def editar_cliente(self):
        return "Cliente editado."

    def gerar_contrato_venda(self):
        return "Contrato de venda gerado."

    def solicitar_ajuste_estoque_administrador(self):
        return "Solicitação de ajuste de estoque enviada ao administrador."

    def registrar_venda(self):
        return "Venda registrada."