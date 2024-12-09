"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from core import views as core_views
from tienda import views as tienda_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name='index'),
    path('about/', core_views.about, name='about'),
    path('creadores/', core_views.creadores, name='creadores'),
    path('gallery/', core_views.galeria, name="galeria"),
    path('productos/', tienda_views.lista_productos, name='lista_productos'),
    path('categoria/<int:categoria_id>/', tienda_views.productos_por_categoria, name='productos_por_categoria'),
    path('agregar-al-carrito/<int:producto_id>/', tienda_views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', tienda_views.ver_carrito, name='ver_carrito'),
    path('eliminar-del-carrito/<int:producto_id>/', tienda_views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', tienda_views.register, name='register'),
    path('carrito/realizar_pedido/', tienda_views.realizar_pedido, name='realizar_pedido'),
    path('login/', tienda_views.CustomLoginView.as_view(), name='login'),  # Vista 'login' de la app 'usuarios'

    
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)