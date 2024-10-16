from django.urls import path
from . import views

urlpatterns = [
    path('', views.transacoes_view, name='transacoes'),
    path('adicionar_receita/', views.adicionar_receita, name='adicionar_receita'),
    path('adicionar_despesa/', views.adicionar_despesa, name='adicionar_despesa'),
    path('adicionar-categoria', views.adicionar_categoria, name='adicionar_categoria'),
    path('excluir_transacao/<int:transacao_id>/', views.excluir_transacao, name='excluir_transacao'),
]