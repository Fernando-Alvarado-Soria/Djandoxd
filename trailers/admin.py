from django.contrib import admin
from .models import Viaje

# Register your models here.

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ['numero_viaje', 'numero_contenedor', 'origen', 'destino', 'pagado', 'costo_viaje', 'ganancia', 'fecha_creacion']
    list_filter = ['fecha_creacion', 'pagado', 'origen', 'destino']
    search_fields = ['numero_viaje', 'numero_contenedor', 'numero_factura', 'origen', 'destino']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Viaje', {
            'fields': ('numero_viaje', 'numero_contenedor', 'numero_factura', 'origen', 'destino')
        }),
        ('Estado de Pago', {
            'fields': ('pagado', 'fecha_pago', 'fecha_viaje')
        }),
        ('Gastos', {
            'fields': ('gastos_casetas', 'gastos_diesel', 'otros_gastos')
        }),
        ('Financiero', {
            'fields': ('costo_viaje', 'ganancia')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

