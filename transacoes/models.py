from django.db import models
from django.conf import settings
import decimal


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

class Receita(models.Model):
    descricao = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descricao} - {self.valor}"

class Despesa(models.Model):
    descricao = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descricao} - {self.valor}"