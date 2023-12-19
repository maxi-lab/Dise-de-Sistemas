from django.db import models
from ventas.models import Venta
from django.utils.timezone import now
# Create your models here.

class Cobranza(models.Model):
    fecha=models.DateField(default=now())
    monto=models.FloatField()
class Efectivo(models.Model):
    monto=models.FloatField()
    CobranzaId=models.ForeignKey(Cobranza,on_delete=models.CASCADE)

class TipoTarjeta(models.TextChoices):
    CREDITO='C','credito'
    DEBITO='D','debito'

class Tarjeta(models.Model):
    cbu=models.IntegerField()
    monto=models.FloatField()
    tipo=models.CharField(max_length=1,
                          choices=TipoTarjeta.choices)
    CobranzaId=models.ForeignKey(Cobranza,on_delete=models.CASCADE)
class TranferenciaBancaria(models.Model):
    cbu=models.IntegerField()
    monto=models.FloatField()
    nroOperacion=models.IntegerField()
    CobranzaId=models.ForeignKey(Cobranza,on_delete=models.CASCADE)

class VentaCobranza(models.Model):
    monto=models.FloatField()
    CobranzaId=models.ForeignKey(Cobranza,on_delete=models.CASCADE)
    VentaId=models.ForeignKey(Venta,on_delete=models.CASCADE)