from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    # Adicionar a classe 'form-control' aos campos do formulário
    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo'].widget.attrs.update({'class': 'form-control'})
        self.fields['montante_plan'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: 500,00'
        })

    class Meta:
        model = Categoria
        fields = ['nome', 'tipo', 'montante_plan']  # Incluir montante_plan
