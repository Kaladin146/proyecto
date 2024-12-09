from django.shortcuts import render



def index(request):
    return render(request,'core/index.html')

def about(request):
    return render(request,'core/about.html')

def galeria(request):
    return render(request,'core/galeria.html')

def creadores(request):
    return render(request,'core/creadores.html')




# Create your views here.
