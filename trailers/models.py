from django.db import models
from django.core.validators import RegexValidator

# ========================
# MODELOS BASE
# ========================

class Cliente(models.Model):
    """Modelo para representar clientes que solicitan viajes"""
    nombre = models.CharField(max_length=200, verbose_name="Nombre del cliente")
    rfc = models.CharField(
        max_length=13, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$',
                message='RFC no válido. Formato: XAXX010101000'
            )
        ],
        verbose_name="RFC"
    )
    activo = models.BooleanField(default=True, verbose_name="Cliente activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.rfc})"


class Operador(models.Model):
    """Modelo para representar operadores/choferes"""
    nombre = models.CharField(max_length=200, verbose_name="Nombre del operador")
    licencia = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Número de licencia"
    )
    activo = models.BooleanField(default=True, verbose_name="Operador activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} (Lic: {self.licencia})"


class Unidad(models.Model):
    """Modelo para representar unidades/vehículos (camiones, tractocamiones)"""
    numero_economico = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Número económico"
    )
    placas = models.CharField(max_length=20, unique=True, verbose_name="Placas")
    marca = models.CharField(max_length=100, verbose_name="Marca")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    anio = models.PositiveIntegerField(verbose_name="Año")
    activo = models.BooleanField(default=True, verbose_name="Unidad activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        ordering = ['numero_economico']

    def __str__(self):
        return f"{self.numero_economico} - {self.marca} {self.modelo} ({self.anio})"


# ========================
# MODELO VIAJE (Se actualizará en Paso 2)
# ========================

class Viaje(models.Model):
    numero_viaje = models.CharField(max_length=100, unique=True, verbose_name="Número de viaje")
    numero_contenedor = models.CharField(max_length=100, blank=True, verbose_name="Número de contenedor")
    numero_factura = models.CharField(max_length=100, blank=True, verbose_name="Número de factura")
    origen = models.CharField(max_length=200, verbose_name="Origen")
    destino = models.CharField(max_length=200, verbose_name="Destino")
    pagado = models.BooleanField(default=False, verbose_name="¿Viaje pagado?")
    fecha_pago = models.DateField(null=True, blank=True, verbose_name="Fecha de pago")
    fecha_viaje = models.DateField(null=True, blank=True, verbose_name="Fecha de viaje")
    gastos_casetas = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Gastos de casetas")
    gastos_diesel = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Gastos de diesel")
    otros_gastos = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Otros gastos")
    costo_viaje = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del viaje")
    ganancia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Ganancia")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.numero_viaje} - {self.origen} a {self.destino}"

    def total_gastos(self):
        return self.gastos_casetas + self.gastos_diesel + self.otros_gastos

