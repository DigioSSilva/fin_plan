from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CategoriaForm
from .models import Categoria
from django.http import JsonResponse
from decimal import Decimal
from django.views.decorators.http import require_POST

@login_required
def planejamento_view(request):
    categorias_despesa = Categoria.objects.filter(tipo='despesa', usuario=request.user)
    context = {'categorias_despesa': categorias_despesa}
    return render(request, 'planejamento/planejamento.html', context)

@login_required
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)

        if form.is_valid():
            nome_categoria = form.cleaned_data['nome'].upper()
            tipo_categoria = form.cleaned_data['tipo']
            montante_plan = form.cleaned_data.get('montante_plan')
            print(f"O montante plan passou por aqui: {montante_plan}")
            # Verifica se a categoria já existe para o tipo especificado
                  
            if Categoria.objects.filter(nome=nome_categoria, tipo=tipo_categoria, usuario=request.user).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'A categoria {nome_categoria} já foi cadastrada para {tipo_categoria}.'
                })

            categoria = form.save(commit=False)
            categoria.nome = nome_categoria
            categoria.usuario = request.user

            #Montante plan apenas para despesas
            if tipo_categoria == 'despesa':
            
                try:
                    categoria.montante_plan = Decimal(str(montante_plan).replace(',', '.'))
                except Exception as e:
                    return JsonResponse({'success': False, 'error': 'Montante inválido.'})
            else: 
                categoria.montan_plan = Decimal('0')

            categoria.save()
            return JsonResponse({'success': True, 'message': 'Categoria salva com sucesso!'})

        return JsonResponse({'success': False, 'error': 'Erro ao salvar categoria. Verifique os dados inseridos.'})

    return JsonResponse({'success': False, 'error': 'Método não permitido.'})


@login_required
def categorias_view(request):
    categorias_despesa = Categoria.objects.filter(tipo='despesa', usuario = request.user)
    context = {'categorias_despesa': categorias_despesa}
    print(categorias_despesa)
    return render(request, 'planejamento/planejamento.html', context)

@require_POST
@login_required
def excluir_categoria(request, categoria_id):
    try:
        # Tenta encontrar a categoria associada ao usuário
        categoria = Categoria.objects.get(id=categoria_id, usuario=request.user)
        categoria.delete()  # Exclui a categoria
        return JsonResponse({'success': True})
    except Categoria.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Categoria não encontrada.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})