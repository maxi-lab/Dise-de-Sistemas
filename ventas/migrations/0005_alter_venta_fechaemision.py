# Generated by Django 5.0 on 2023-12-20 20:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0004_rename_condiciondepagoid_condiciondepagoarticulo_condiciondepago_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='fechaEmision',
            field=models.DateField(default=datetime.date(2023, 12, 20)),
        ),
    ]
