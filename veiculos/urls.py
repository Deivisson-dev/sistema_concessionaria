from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    path('', views.VeiculoListView.as_view(), name='listar'),
    path('novo/', views.VeiculoCreateView.as_view(), name='criar'),
    path('editar/<int:pk>/', views.VeiculoUpdateView.as_view(), name='editar'),
    path('excluir/<int:pk>/', views.VeiculoDeleteView.as_view(), name='excluir'),
    path('detalhes/<int:pk>/', views.VeiculoDetailView.as_view(), name='detalhes'),

]