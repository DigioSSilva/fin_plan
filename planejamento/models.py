from django.db import models
from django.conf import settings

class Categoria(models.Model):
    tipo_coices = (
        ('receita', 'Receita'), 
        ('despesa', 'Despesa'),
    )
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=tipo_coices)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.nome} - {self.tipo}'