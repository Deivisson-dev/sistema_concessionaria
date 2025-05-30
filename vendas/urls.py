from django.urls import path
from . import views
from .views import gerar_contrato_pdf


app_name = 'vendas'

urlpatterns = [
    path('', views.VendaListView.as_view(), name='listar'),
    path('novo/', views.VendaCreateView.as_view(), name='criar'),
    path('editar/<int:pk>/', views.VendaUpdateView.as_view(), name='editar'),
    path('excluir/<int:pk>/', views.VendaDeleteView.as_view(), name='excluir'),
    path('detalhes/<int:pk>/', views.VendaDetailView.as_view(), name='detalhes'),
    path('contrato/<int:pk>/', gerar_contrato_pdf, name='gerar_contrato'),
]