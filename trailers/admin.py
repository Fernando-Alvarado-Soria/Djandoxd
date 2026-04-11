from django.contrib import admin
from .models import Cliente, Operador, Unidad, Viaje

# ========================
# ADMIN MODELOS BASE
# ========================

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rfc', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'rfc']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'rfc', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'licencia', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'licencia']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Operador', {
            'fields': ('nombre', 'licencia', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ['numero_economico', 'placas', 'marca', 'modelo', 'anio', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'marca', 'anio', 'fecha_creacion']
    search_fields = ['numero_economico', 'placas', 'marca', 'modelo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('numero_economico', 'placas', 'activo')
        }),
        ('Especificaciones', {
            'fields': ('marca', 'modelo', 'anio')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


# ========================
# ADMIN VIAJE
# ========================

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

