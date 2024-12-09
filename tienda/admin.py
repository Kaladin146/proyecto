from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import TruncWeek
from django.urls import path
from django.shortcuts import render
from .models import Categoria, Producto, Pedido, PedidoAceptado, PedidoRechazado,Venta
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.template.loader import get_template
from xhtml2pdf import pisa 
from django.http import HttpResponse


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'categoria')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('categoria',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'total', 'fecha', 'estado', 'direccion', 'telefono', 'mostrar_productos')
    search_fields = ('usuario__username', 'direccion', 'codigo_postal', 'telefono', 'email')
    list_filter = ('fecha', 'estado')
    actions = ['aceptar_pedidos', 'rechazar_pedidos','marcar_como_notificado']

    def mostrar_productos(self, obj):
        productos = obj.productos
        if productos:
            return ", ".join([f"{item['titulo']} (x{item['cantidad']})" for item in productos.values()])
        return "No hay productos"
    mostrar_productos.short_description = "Productos solicitados"

    @admin.action(description='Aceptar pedidos seleccionados')
    def aceptar_pedidos(self, request, queryset):
        queryset.update(estado='aceptado')

    @admin.action(description='Rechazar pedidos seleccionados')
    def rechazar_pedidos(self, request, queryset):
        queryset.update(estado='rechazado')
        
    def marcar_como_notificado(self, request, queryset):
        queryset.update(notificado=True)
        self.message_user(request, "Los pedidos seleccionados han sido marcados como notificados.")

    marcar_como_notificado.short_description = "Marcar como notificados"    

    # Definir la URL personalizada para ventas semanales
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ventas-semanales/', self.admin_site.admin_view(self.ventas_semanales), name='ventas_semanales'),
        ]
        return custom_urls + urls

    def ventas_semanales(self, request):
        # Agrupar pedidos aceptados por semana
        pedidos_semanales = (
            Pedido.objects.filter(estado='aceptado')
            .annotate(semana=TruncWeek('fecha'))
            .values('semana')
            .annotate(total_ventas=Sum('total'))
            .order_by('-semana')
        )

        # Pasar los datos de ventas semanales al template
        return render(
            request,
            'admin/ventas_semanales.html',
            {'pedidos_semanales': pedidos_semanales}
        )


class PedidoAceptadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'total', 'fecha', 'direccion', 'telefono', 'mostrar_productos')
    search_fields = ('usuario__username', 'direccion', 'telefono', 'email')
    list_filter = ('fecha',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(estado='aceptado')

    def mostrar_productos(self, obj):
        productos = obj.productos
        if productos:
            return ", ".join([f"{item['titulo']} (x{item['cantidad']})" for item in productos.values()])
        return "No hay productos"
    mostrar_productos.short_description = "Productos solicitados"

class PedidoRechazadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'total', 'fecha', 'direccion', 'telefono', 'mostrar_productos')
    search_fields = ('usuario__username', 'direccion', 'telefono', 'email')
    list_filter = ('fecha',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(estado='rechazado')

    def mostrar_productos(self, obj):
        productos = obj.productos
        if productos:
            return ", ".join([f"{item['titulo']} (x{item['cantidad']})" for item in productos.values()])
        return "No hay productos"
    mostrar_productos.short_description = "Productos solicitados"
    
@admin.action(description='Generar Reporte PDF de Ventas')
def generar_reporte_ventas(modeladmin, request, queryset):
    ventas = queryset  # Filtrar las ventas seleccionadas en el admin
    template_path = 'reporte_ventas.html'  # Plantilla para el PDF
    context = {'ventas': ventas, 'total_ventas': sum(v.total for v in ventas)}

    # Renderizar plantilla
    template = get_template(template_path)
    html = template.render(context)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el reporte PDF', status=500)
    return response

# Registrar el modelo con la acción personalizada}
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'precio_unitario', 'total', 'fecha')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generar-reporte/', self.admin_site.admin_view(self.generar_reporte_todas_ventas), name='reporte_ventas'),
        ]
        return custom_urls + urls

    def generar_reporte_todas_ventas(self, request):
        ventas = Venta.objects.all()
        template_path = 'tienda/reporte_ventas.html'
        context = {'ventas': ventas, 'total_ventas': sum(v.total for v in ventas)}

        template = get_template(template_path)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error al generar el reporte PDF', status=500)
        return response

# Registro de modelos en el admin de Django
admin.site.site_header = "Panel de Administrador"
admin.site.site_title = "Administración de Mi Proyecto"
admin.site.index_title = "Bienvenido al Panel de Control"
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(PedidoAceptado, PedidoAceptadoAdmin)
admin.site.register(PedidoRechazado, PedidoRechazadoAdmin)
