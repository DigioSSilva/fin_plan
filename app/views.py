from django.shortcuts import render
from django.http import HttpResponse

def test_login(request):
    return render(request, 'registration/login.html')
