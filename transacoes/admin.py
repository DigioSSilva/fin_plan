from django.contrib import admin
from .models import Categoria, Receita, Despesa

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'usuario')  # Campos a serem exibidos
    list_filter = ('tipo',)  # Filtro lateral por tipo
    search_fields = ('nome',)  # Busca por nome

class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'usuario')  # Campos a serem exibidos
    search_fields = ('descricao',)  # Busca por descrição

class DespesaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'usuario')  # Campos a serem exibidos
    search_fields = ('descricao',)  # Busca por descrição

# Registra os modelos com suas respectivas classes Admin
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Receita, ReceitaAdmin)
admin.site.register(Despesa, DespesaAdmin)
