from django.urls import path
from . import views

urlpatterns = [
    path('', views.planejamento_view, name='planejamento'),
    path('adicionar-categoria', views.adicionar_categoria, name='adicionar_categoria'),
    path('excluir_categoria/<int:categoria_id>/', views.excluir_categoria, name='excluir_categoria'),
     path('categorias/', views.categorias_view, name='categorias_view'),
]
