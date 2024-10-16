from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirecionar para o dashboard após o registro
        else:
            print(form.errors)  # Exiba os erros no console
    else:
        form = CustomUserCreationForm()
        print("GET request")
    return render(request, 'users/register.html', {'form': form})

