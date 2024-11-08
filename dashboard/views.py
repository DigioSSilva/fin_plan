from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.utils import financial_data

@login_required
def dashboard(request):
    context = financial_data(
        request,
        selected_month=request.GET.get('month'),
        selected_year=request.GET.get('year')
    )
    return render(request, 'dashboard/dashboard.html', context)