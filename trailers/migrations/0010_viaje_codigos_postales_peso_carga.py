# Generated manually because the local virtualenv Python is not executable.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trailers', '0009_alter_viaje_precio_diesel_litro'),
    ]

    operations = [
        migrations.AddField(
            model_name='viaje',
            name='codigo_postal_origen',
            field=models.CharField(blank=True, max_length=10, verbose_name='Código postal de origen'),
        ),
        migrations.AddField(
            model_name='viaje',
            name='codigo_postal_destino',
            field=models.CharField(blank=True, max_length=10, verbose_name='Código postal de destino'),
        ),
        migrations.AddField(
            model_name='viaje',
            name='peso_carga',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Peso adicional de la carga'),
        ),
        migrations.AddField(
            model_name='viaje',
            name='unidad_peso',
            field=models.CharField(choices=[('kg', 'Kilogramos'), ('ton', 'Toneladas'), ('lb', 'Libras')], default='kg', max_length=3, verbose_name='Unidad de peso'),
        ),
    ]
