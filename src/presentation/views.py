from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def becas(request):
    return render(request, 'becas.html')
