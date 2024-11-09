from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
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
        fields = ['nome', 'tipo', 'montante_plan'] 
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        montante_plan = cleaned_data.get('montante_plan')

        # Se for 'receita', ignorar a validação do montante_plan
        if tipo == 'despesa':
            if montante_plan is None or montante_plan <= 0:
                self.add_error(
                    'montante_plan', 
                    'Por favor, insira um montante estimado de gastos para a categoria de despesa.'
                )

        return cleaned_data