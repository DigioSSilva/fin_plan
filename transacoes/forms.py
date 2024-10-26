from django import forms
from .models import Receita, Despesa, Categoria

class ReceitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Obtenha o usuário do kwargs
        super(ReceitaForm, self).__init__(*args, **kwargs)
        if self.user:  # Verifique se o usuário foi fornecido
            self.fields['categoria'].queryset = Categoria.objects.filter(tipo='receita', usuario=self.user)
            self.fields['descricao'].widget.attrs.update({'placeholder': 'Ex: Salário', 'class': 'form-control'})
            self.fields['categoria'].widget.attrs.update({'placeholder': 'Ex: Categoria', 'class': 'form-control'})
            self.fields['data'].widget.attrs.update({'placeholder': 'dd/mm/aaaa', 'class': 'form-control'})
            self.fields['valor'].widget.attrs.update({'placeholder': 'Ex: 1500,00', 'class': 'form-control'})

    #def clean_valor(self):
       # valor = self.cleaned_data.get('valor')  # Usar get para evitar KeyError
       # if valor is None:
           # raise ValidationError('Este campo é obrigatório.')
        
        #try:
            # Converter o valor para decimal
            #valor = str(valor).replace(',', '.') 
            #return Decimal(valor)
        #except (ValueError, TypeError, decimal.InvalidOperation) as e:
            #raise ValidationError(f'Valor inválido: {str(e)}')  

    class Meta:
        model = Receita
        fields = ['descricao', 'categoria', 'data', 'valor']

class DespesaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DespesaForm, self).__init__(*args, **kwargs)
        if self.user: 
            self.fields['categoria'].queryset = Categoria.objects.filter(tipo='despesa', usuario=self.user)
            self.fields['descricao'].widget.attrs.update({'placeholder': 'Ex: Supermercado', 'class': 'form-control'})
            self.fields['categoria'].widget.attrs.update({'placeholder': 'Ex: Alimentação', 'class': 'form-control'})
            self.fields['data'].widget.attrs.update({'placeholder': 'dd/mm/aaaa', 'class': 'form-control'})
            self.fields['valor'].widget.attrs.update({'placeholder': 'Ex: 150,00', 'class': 'form-control'}) 

    class Meta:
        model = Despesa
        fields = ['descricao', 'categoria', 'data', 'valor']

class EditarTransacaoForm(forms.ModelForm):
    class Meta:
        model = Receita  # Ou Despesa, dependendo do tipo de transação
        fields = ['descricao', 'valor', 'categoria', 'data']

class ExcluirTransacaoForm(forms.Form):
    # Campo oculto para armazenar o ID da transação
    transacao_id = forms.IntegerField(widget=forms.HiddenInput()) 