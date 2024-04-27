from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def binario_binario(request):
    return render(request, 'binario_binario.html')
