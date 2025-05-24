from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='listar'),
    path('novo/', views.ClienteCreateView.as_view(), name='criar'),
    path('editar/<int:pk>/', views.ClienteUpdateView.as_view(), name='editar'),
    path('excluir/<int:pk>/', views.ClienteDeleteView.as_view(), name='excluir'),
]