from django.db import models

# Create your models here.

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

