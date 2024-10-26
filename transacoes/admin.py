from django.contrib import admin
from .models import Categoria, Receita, Despesa



class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'usuario')  # Campos a serem exibidos
    search_fields = ('descricao',)  # Busca por descrição

class DespesaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'usuario')  # Campos a serem exibidos
    search_fields = ('descricao',)  # Busca por descrição

# Registra os modelos com suas respectivas classes Admin

admin.site.register(Receita, ReceitaAdmin)
admin.site.register(Despesa, DespesaAdmin)
