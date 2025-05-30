from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from vendas.models import Venda

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/listar.html'
    context_object_name = 'clientes'

class ClienteCreateView(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:listar')
    success_message = "Cliente cadastrado com sucesso!"

    

class ClienteUpdateView(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:listar')
    success_message = "Dados do cliente atualizados!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/confirmar_exclusao.html'
    success_url = reverse_lazy('clientes:listar')
    
    def get_queryset(self):
        return Cliente.all_objects.all()
    
    def form_valid(self, form):
        if self.object.venda_set.exists():
            messages.error(
                self.request,
                "Este cliente está vinculado a vendas e não pode ser excluído!",
                extra_tags='danger'
            )
            return HttpResponseRedirect(self.get_success_url())
        
        self.object.soft_delete()
        messages.success(self.request, "Cliente excluído com sucesso!")
        return HttpResponseRedirect(self.get_success_url())
    
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/detalhes.html'
    context_object_name = 'cliente'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona histórico de compras do cliente
        context['vendas'] = Venda.objects.filter(cliente=self.object)
        return context