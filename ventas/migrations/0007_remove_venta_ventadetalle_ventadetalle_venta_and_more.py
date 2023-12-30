# Generated by Django 5.0 on 2023-12-21 20:44

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_alter_condiciondepago_tipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='VentaDetalle',
        ),
        migrations.AddField(
            model_name='ventadetalle',
            name='Venta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ventas.venta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='venta',
            name='fechaEmision',
            field=models.DateField(default=datetime.date(2023, 12, 21)),
        ),
    ]