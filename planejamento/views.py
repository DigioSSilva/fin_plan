from django.shortcuts import render
from django.http import HttpResponse

def planejamento(request):
  html = """
  <!DOCTYPE html>
  <html>
  <head>
    <title>Teste</title>
  </head>
  <body>
    <h1>Se aparecer bora Brinão, funcionou!</h1>
  </body>
  </html>
  """
  return HttpResponse(html)
