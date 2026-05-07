from django.db import migrations


TIPOS_UNIDAD = [
    # (nombre, descripcion, rendimiento_km_litro)
    (
        "Pick-up / Estacas (1-3.5 ton)",
        "Vehículo ligero para entregas locales y última milla. Capacidad de 1 a 3.5 toneladas.",
        9.00,
    ),
    (
        "Rabón C2 (8-10 ton)",
        "Camión de 2 ejes. Ideal para distribución regional. Carga aproximada de 8 a 10 toneladas.",
        6.00,
    ),
    (
        "Torton C3 (15-20 ton)",
        "Camión de 3 ejes (1 delantero + 2 traseros). 'Caballito de batalla' para viajes interregionales. Carga de 15 a 20 toneladas.",
        4.50,
    ),
    (
        "Caja Seca Sencillo (25-30 ton)",
        "Tractocamión con un semirremolque de caja seca (sin temperatura controlada). Capacidad de 25 a 30 toneladas.",
        3.50,
    ),
    (
        "Refrigerado / Termo Sencillo (25-30 ton)",
        "Tractocamión con semirremolque refrigerado para alimentos perecederos o medicamentos. Capacidad de 25 a 30 toneladas.",
        3.00,
    ),
    (
        "Plataforma Sencillo (25-30 ton)",
        "Tractocamión con plataforma abierta para material de construcción, estructuras de acero o maquinaria pesada.",
        3.50,
    ),
    (
        "Full / Doble Remolque (50-60 ton)",
        "Dos cajas arrastradas por un solo tractor (normado por NOM-012). Máxima capacidad de carga, hasta 50-60 toneladas.",
        2.50,
    ),
    (
        "Autotanque / Pipa",
        "Tractocamión con tanque para transporte de líquidos, químicos o combustibles.",
        3.50,
    ),
    (
        "Jaula (Ganado / Agrícola)",
        "Unidad con jaula abierta para transporte de animales vivos o productos agrícolas a granel.",
        4.00,
    ),
]


def seed_tipos(apps, schema_editor):
    TipoUnidad = apps.get_model('trailers', 'TipoUnidad')
    for nombre, descripcion, rendimiento in TIPOS_UNIDAD:
        TipoUnidad.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion, 'rendimiento_km_litro': rendimiento},
        )


def delete_tipos(apps, schema_editor):
    TipoUnidad = apps.get_model('trailers', 'TipoUnidad')
    TipoUnidad.objects.filter(nombre__in=[t[0] for t in TIPOS_UNIDAD]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('trailers', '0007_tipounidad_viaje_tipo_unidad'),
    ]

    operations = [
        migrations.RunPython(seed_tipos, delete_tipos),
    ]
