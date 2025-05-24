from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib import messages

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
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())