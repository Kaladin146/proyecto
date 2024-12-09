from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings



def index(request):
    return render(request,'core/index.html')

def about(request):
    return render(request,'core/about.html')

def galeria(request):
    return render(request,'core/galeria.html')

def contactanos(request):
    message = None
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        # Formar el mensaje de correo
        mensaje_completo = f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}"

        # Enviar correo
        send_mail(
            'Nuevo mensaje de contacto',  # Asunto
            mensaje_completo,            # Cuerpo
            settings.DEFAULT_FROM_EMAIL, # De
            [settings.DEFAULT_FROM_EMAIL], # Para (destinatario)
        )
        message = "¡Tu mensaje ha sido enviado con éxito!"

    return render(request, 'core/contactanos.html', {'message': message})

# Create your views here.
