from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Receita, Despesa, Categoria
from .forms import ReceitaForm, DespesaForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import JsonResponse
from app.utils import financial_data
from datetime import datetime



@login_required
def adicionar_receita(request):
    if request.method == 'POST':
        data = request.POST.copy()
        # Trocar vírgula por ponto no valor
        data['valor'] = data['valor'].replace(',', '.')
        form = ReceitaForm(data, user=request.user)

        if form.is_valid():
            descricao = form.cleaned_data['descricao'].capitalize()
            valor = Decimal(form.cleaned_data['valor'])
            data_receita = form.cleaned_data['data']
            categoria = form.cleaned_data['categoria']

            # Verificar se já existe uma receita com a mesma descrição, data e valor
            if Receita.objects.filter(
                descricao=descricao,
                data=data_receita,
                valor=valor,
                categoria=categoria,
                usuario=request.user
            ).exists():
                return JsonResponse({'success': False, 'message': 'Receita já registrada.'})

            receita = form.save(commit=False)
            receita.usuario = request.user
            receita.descricao = descricao
            receita.valor = valor
            receita.save()

            return JsonResponse({'success': True, 'message': 'Receita salva com sucesso!'})

        else:
            # Enviar os erros de validação do formulário
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = ReceitaForm(user=request.user)
        return render(request, 'transacoes/adicionar_receita.html', {'form': form})



@login_required
def adicionar_despesa(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['valor'] = data['valor'].replace(',', '.')
        
        form = DespesaForm(data, user=request.user)

        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.descricao = despesa.descricao.capitalize()
            
            # Formatar valor para Decimal
            despesa.valor = Decimal(data['valor'])
            
            despesa.save()

            # Resposta AJAX em caso de sucesso
            response_data = {'success': True, 'message': 'Despesa salva com sucesso!'}
            return JsonResponse(response_data)

        else:
            # Resposta AJAX em caso de erros de validação
            response_data = {'success': False, 'errors': form.errors}
            return JsonResponse(response_data)

    else:
        # Preparar formulário e categorias para renderização inicial do modal
        form = DespesaForm(user=request.user)
        categorias_despesa = Categoria.objects.filter(tipo='despesa', usuario=request.user)

        context = {
            'form': form,
            'categorias_despesa': categorias_despesa,
        }
        return render(request, 'transacoes/adicionar_despesa.html', context)



@login_required
def transacoes_view(request):
    categorias_receita = Categoria.objects.filter(tipo='receita', usuario=request.user)
    categorias_despesa = Categoria.objects.filter(tipo='despesa', usuario=request.user)

    #Filtrar 10 mais recentes (mudar a lógica posteriormente)
    receitas = Receita.objects.filter(usuario=request.user).order_by('-data')
    despesas = Despesa.objects.filter(usuario=request.user).order_by('-data')

    for receita in receitas:
        receita.tipo = 'receita'
    for despesa in despesas:
        despesa.tipo = 'despesa'

    transacoes = list(receitas) + list(despesas)
    transacoes.sort(key=lambda transacao: transacao.data, reverse=True)

    context = {
        'categorias_receita': categorias_receita,
        'categorias_despesa': categorias_despesa,
        'transacoes': transacoes
    }
    #Lógica para valores dos saldos no topo da pagina
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    financial_context = financial_data(
        request,
        selected_month=current_month,
        selected_year=current_year
    )
    context.update(financial_context)
    return render (request, 'transacoes/transacoes.html', context)

@login_required
def editar_transacao(request, transacao_id):
    """
    View para editar uma transação (receita ou despesa).
    """
    try:
        # Tenta buscar a transação como Receita
        transacao = get_object_or_404(Receita, pk=transacao_id, usuario=request.user)
        form_class = ReceitaForm
        categorias = Categoria.objects.filter(tipo='receita', usuario=request.user)
    except Receita.DoesNotExist:
        try:
            # Se não encontrar como Receita, tenta buscar como Despesa
            transacao = get_object_or_404(Despesa, pk=transacao_id, usuario=request.user)
            form_class = DespesaForm
            categorias = Categoria.objects.filter(tipo='despesa', usuario=request.user)
        except Despesa.DoesNotExist:
            # Se não encontrar como Despesa, retorna um erro 404
            return JsonResponse({'success': False, 'error': 'Transação não encontrada.'}, status=404)

    if request.method == 'POST':
        # Converter a vírgula para ponto no valor, se necessário
        data = request.POST.copy()
        data['valor'] = data['valor'].replace(',', '.')

        # Criar o formulário com os dados da requisição POST
        form = form_class(data, instance=transacao, user=request.user)

        if form.is_valid():
            # Salvar a transação editada
            transacao = form.save(commit=False)

            # Converter a descrição para capitalizar apenas a primeira letra
            transacao.descricao = transacao.descricao.capitalize()

            # Converter a categoria para maiúsculas (opcional)
            transacao.categoria.nome = transacao.categoria.nome.upper()

            transacao.save()

            return JsonResponse({'success': True, 'message': 'Transação editada com sucesso!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    else:  # Requisição GET
        # Criar o formulário com os dados da transação
        form = form_class(instance=transacao, user=request.user)

        context = {
            'transacao': transacao,
            'form': form,
            'categorias': categorias,
        }
        return render(request, 'transacoes/editar_transacao.html', context)


@require_POST
@login_required
def excluir_transacao(request, transacao_id):
    """
    View para excluir uma transação (receita ou despesa) via AJAX.
    """
    tipo = request.POST.get('tipo')
    
    if tipo not in ['receita', 'despesa']:
        return JsonResponse({'success': False, 'error': 'Tipo de transação inválido.'}, status=400)

    # Usar get_object_or_404 para obter a transação
    if tipo == 'receita':
        transacao = get_object_or_404(Receita, pk=transacao_id, usuario=request.user)
    elif tipo == 'despesa':
        transacao = get_object_or_404(Despesa, pk=transacao_id, usuario=request.user)

    # Excluindo a transação
    transacao.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'{tipo.capitalize()} excluída com sucesso!'
    })