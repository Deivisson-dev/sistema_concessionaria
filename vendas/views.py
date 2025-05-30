from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Venda
from .forms import VendaForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class VendaListView(ListView):
    model = Venda
    template_name = 'vendas/listar.html'
    context_object_name = 'vendas'
    ordering = ['-data_venda']

class VendaCreateView(SuccessMessageMixin, CreateView):
    model = Venda
    form_class = VendaForm
    template_name = 'vendas/form.html'
    success_url = reverse_lazy('vendas:listar')
    success_message = "Venda registrada com sucesso!"

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Erro no registro! Verifique os campos destacados.",
            extra_tags='danger'
        )
        return super().form_invalid(form)

class VendaUpdateView(SuccessMessageMixin, UpdateView):
    model = Venda
    form_class = VendaForm
    template_name = 'vendas/form.html'
    success_url = reverse_lazy('vendas:listar')
    success_message = "Venda atualizada com sucesso!"

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Erro na atualização! Verifique os campos destacados.",
            extra_tags='danger'
        )
        return super().form_invalid(form)

class VendaDeleteView(DeleteView):
    model = Venda
    template_name = 'vendas/confirmar_exclusao.html'
    success_url = reverse_lazy('vendas:listar')
    
    def get_queryset(self):
        """Usa o manager que inclui todos os registros (até os deletados)"""
        return Venda.all_objects.all()
    
    def form_valid(self, form):
        """Executa o soft delete e reverte o status do veículo"""
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
    

class VendaDetailView(DetailView):
    model = Venda
    template_name = 'vendas/detalhes.html'
    context_object_name = 'venda'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
def gerar_contrato_pdf(request, pk):
    venda = Venda.objects.get(pk=pk)
    
    buffer = io.BytesIO()
    
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    styles = getSampleStyleSheet()
    p.setTitle(f"Contrato de Venda #{venda.id}")
    
    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height-50, "CONTRATO DE VENDA DE VEÍCULO")
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height-80, f"Contrato Nº: {venda.id}")
    
    # Dados do contrato
    y_position = height - 120
    
    # Informações das partes
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "VENDEDOR:")
    p.setFont("Helvetica", 12)
    p.drawString(150, y_position, "Concessionária XYZ LTDA")
    
    y_position -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "COMPRADOR:")
    p.setFont("Helvetica", 12)
    p.drawString(150, y_position, venda.cliente.nome)
    
    # Tabela de dados do veículo
    y_position -= 60
    veiculo_data = [
        ["Marca", venda.veiculo.marca],
        ["Modelo", venda.veiculo.modelo],
        ["Ano Fabricação", venda.veiculo.ano_fabricacao],
        ["Placa", venda.veiculo.placa],
        ["Chassi", venda.veiculo.chassi],
        ["Cor", venda.veiculo.cor]
    ]
    
    table = Table(veiculo_data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'Helvetica', 12),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    table.wrapOn(p, width-100, height)
    table.drawOn(p, 50, y_position - table._height)
    
    # Detalhes da transação
    y_position -= table._height + 40
    transacao_data = [
        ["Valor do Veículo", f"R$ {venda.valor:,.2f}"],
        ["Forma de Pagamento", venda.get_forma_pagamento_display()],
        ["Data da Venda", venda.data_venda.strftime("%d/%m/%Y")]
    ]
    
    table = Table(transacao_data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'Helvetica', 12),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    table.wrapOn(p, width-100, height)
    table.drawOn(p, 50, y_position - table._height)
    
    # Cláusulas do contrato
    y_position -= table._height + 60
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "CLÁUSULAS E CONDIÇÕES:")
    
    clausulas = [
        "1. O veículo é vendido no estado em que se encontra, sem garantia expressa ou implícita.",
        "2. O comprador declara ter examinado o veículo e aceita suas condições.",
        "3. O vendedor não se responsabiliza por vícios ocultos.",
        "4. O pagamento será feito conforme forma acordada acima.",
        "5. O veículo será entregue após confirmação do pagamento."
    ]
    
    p.setFont("Helvetica", 12)
    for i, clausula in enumerate(clausulas):
        y_position -= 20
        p.drawString(70, y_position, clausula)
    
    # Assinaturas
    y_position -= 100
    p.line(100, y_position, 250, y_position)
    p.drawString(100, y_position - 20, "Assinatura do Vendedor")
    
    p.line(350, y_position, 500, y_position)
    p.drawString(350, y_position - 20, "Assinatura do Comprador")
    
    # Data e local
    y_position -= 60
    p.drawString(100, y_position, f"Data: {venda.data_venda.strftime('%d/%m/%Y')}")
    p.drawString(100, y_position - 20, "Local: Concessionária XYZ")
    
    # Finaliza o PDF
    p.showPage()
    p.save()
    
    # Configura a resposta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_venda_{venda.id}.pdf"'
    return response