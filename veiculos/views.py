from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Veiculo
from .forms import VeiculoForm
from django.http import HttpResponseRedirect


class VeiculoListView(ListView):
    model = Veiculo
    template_name = 'veiculos/listar.html'
    context_object_name = 'veiculos'

class VeiculoCreateView(SuccessMessageMixin, CreateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculos/form.html'
    success_url = reverse_lazy('veiculos:listar')
    success_message = "Veículo cadastrado com sucesso!"

class VeiculoUpdateView(SuccessMessageMixin, UpdateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculos/form.html'
    success_url = reverse_lazy('veiculos:listar')
    success_message = "Veículo atualizado com sucesso!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

class VeiculoDeleteView(DeleteView):
    model = Veiculo
    template_name = 'veiculos/confirmar_exclusao.html'
    success_url = reverse_lazy('veiculos:listar')

    def get_queryset(self):
        return Veiculo.all_objects.all()
    
    def form_valid(self, form):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
