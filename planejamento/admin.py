from django.contrib import admin
from .models import Categoria

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'montante_plan', 'usuario')  # Campos a serem exibidos
    list_filter = ('tipo',)  # Filtro lateral por tipo
    search_fields = ('nome',)  # Busca por nome


admin.site.register(Categoria, CategoriaAdmin)