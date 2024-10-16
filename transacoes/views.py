from django.shortcuts import render, redirect, get_object_or_404
from .models import Receita, Despesa, Categoria
from .forms import ReceitaForm, DespesaForm, CategoriaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.http import JsonResponse, HttpResponse


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
            despesa.categoria.nome = despesa.categoria.nome.upper()
            valor_formatado = form.cleaned_data['valor']
            valor_sem_formato = str(valor_formatado).replace('R$ ', '')
            despesa.valor = Decimal(valor_sem_formato)
            despesa.save()

            response_data = {'success': True, 'message': 'Despesa salva com sucesso!'}
            return JsonResponse(response_data)

        else:
            response_data = {'success': False, 'errors': form.errors}
            return JsonResponse(response_data)
    
    else:
        form = DespesaForm(user=request.user)
    
        categorias_despesa = Categoria.objects.filter(tipo='despesa', usuario=request.user)
        context = {'form': form, 'categorias_despesa': categorias_despesa}
        return render(request, 'transacoes/adicionar_despesa.html', context)


@login_required
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nome_categoria = form.cleaned_data['nome'].upper()  # Converte o nome para maiúsculas
            tipo_categoria = form.cleaned_data['tipo']
            
            # Verifica se a categoria já existe para o tipo especificado
            if Categoria.objects.filter(nome=nome_categoria, tipo=tipo_categoria, usuario=request.user).exists():
                return JsonResponse({'success': False, 'error': f'A categoria {nome_categoria} já foi cadastrada para {tipo_categoria}.'})
            
            categoria = form.save(commit=False)  # Não salva a categoria ainda
            categoria.nome = nome_categoria  # Atribui o nome em maiúsculas
            categoria.usuario = request.user  # Associa o usuário à categoria
            categoria.save()  # Salva a categoria

            return JsonResponse({'success': True, 'message': 'Categoria salva com sucesso!'})
        
        return JsonResponse({'success': False, 'error': 'Erro ao salvar categoria. Verifique os dados inseridos.'})

    return JsonResponse({'success': False, 'error': 'Método não permitido.'})

@login_required
def transacoes_view(request):
    categorias_receita = Categoria.objects.filter(tipo='receita', usuario=request.user)
    categorias_despesa = Categoria.objects.filter(tipo='despesa', usuario=request.user)

    #Filtrar 10 mais recentes (mudar a lógica posteriormente)
    receitas = Receita.objects.filter(usuario=request.user).order_by('-data')[:10]
    despesas = Despesa.objects.filter(usuario=request.user).order_by('-data')[:10]

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


@login_required
def excluir_transacao(request, transacao_id):
    """
    View para excluir uma transação (receita ou despesa) via AJAX.
    """
    tipo = request.POST.get('tipo')
    if tipo == 'receita':
        transacao = get_object_or_404(Receita, pk=transacao_id, usuario=request.user)
    elif tipo == 'despesa':
        transacao = get_object_or_404(Despesa, pk=transacao_id, usuario=request.user)
    else:
        return JsonResponse({'success': False, 'error': 'A transação já foi excluída. Atualize a página.'}, status=400)
    transacao.delete()
    return JsonResponse({'success': True, 'message': f'{tipo.capitalize()} excluída com sucesso!'})