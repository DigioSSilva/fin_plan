from datetime import datetime
from transacoes.models import Receita, Despesa
from planejamento.models import Categoria
from django.shortcuts import render
from django.db.models import Sum

def financial_data(request, selected_month=None, selected_year=None):
    now = datetime.now()
    months = [
        {'value': 1, 'label': 'Janeiro'},
        {'value': 2, 'label': 'Fevereiro'},
        {'value': 3, 'label': 'Março'},
        {'value': 4, 'label': 'Abril'},
        {'value': 5, 'label': 'Maio'},
        {'value': 6, 'label': 'Junho'},
        {'value': 7, 'label': 'Julho'}, 
        {'value': 8, 'label': 'Agosto'},  
        {'value': 9, 'label': 'Setembro'},  
        {'value': 10, 'label': 'Outubro'},  
        {'value': 11, 'label': 'Novembro'},  
        {'value': 12, 'label': 'Dezembro'}
    ]
    years = range(2023, now.year + 1)

    current_month = int(selected_month) if selected_month else now.month
    current_year = int(selected_year) if selected_year else now.year

    # Buscar as receitas e despesas do mês
    receitas_mes = Receita.objects.filter(
        data__month=current_month, 
        data__year=current_year, 
        usuario=request.user
    )
    despesas_mes = Despesa.objects.filter(
        data__month=current_month, 
        data__year=current_year, 
        usuario=request.user
    )

    total_receitas = sum(receita.valor for receita in receitas_mes) or 0
    total_despesas = sum(despesa.valor for despesa in despesas_mes) or 0

    #Buscar as despesas do mes por categoria
    despesas_por_categoria = Despesa.objects.filter(
        data__month = current_month, 
        data__year = current_year, 
        usuario = request.user
    ).values('categoria__nome').annotate(total=Sum('valor'))


    categorias = [despesa['categoria__nome'] for despesa in despesas_por_categoria]
    totais = [float(despesa['total']) for despesa in despesas_por_categoria]

    #Buscar montante total planejado
    total_planejamento = Categoria.objects.filter(tipo= 'despesa', 
                                                  usuario=request.user
                                                  ).aggregate(Sum('montante_plan'))['montante_plan__sum'] or 0

    #Saldo Atual e saldo planejado
    saldo_atual = total_receitas - total_despesas
    saldo_planejado = total_receitas - total_planejamento

    return {
        'now': now,
        'months': months,
        'years': years,
        'current_month': current_month,
        'current_year': current_year,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'total_planejamento': total_planejamento,
        'saldo_atual': saldo_atual,
        'saldo_planejado': saldo_planejado,
        'categorias': categorias,
        'totais': totais,
    }