from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trailers', '0010_viaje_codigos_postales_peso_carga'),
    ]

    operations = [
        migrations.AddField(
            model_name='viaje',
            name='operador',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='trailers.operador',
                verbose_name='Chofer',
            ),
        ),
        migrations.AlterField(
            model_name='viaje',
            name='peso_carga',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name='Peso de la carga',
            ),
        ),
    ]
