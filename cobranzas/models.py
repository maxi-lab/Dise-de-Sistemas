from django.db import models
from ventas.models import Venta
from django.utils.timezone import now
from django.core.exceptions import ValidationError
# Create your models here.

class Cobranza(models.Model):
    fecha=models.DateField(default=now())
    monto=models.FloatField()
class Efectivo(models.Model):
    monto=models.FloatField()
    Cobranza=models.ForeignKey(Cobranza,on_delete=models.CASCADE)
    def to_jason(self):
        return{
            'monto':self.monto,
            'metodo':'efectivo',
            'id':0,
        }

class TipoTarjeta(models.TextChoices):
    CREDITO='C','credito'
    DEBITO='D','debito'

class Tarjeta(models.Model):
    cbu=models.IntegerField()
    monto=models.FloatField()
    tipo=models.CharField(max_length=1,
                          choices=TipoTarjeta.choices)
    Cobranza=models.ForeignKey(Cobranza,on_delete=models.CASCADE)
    def to_json(self):
        return{
            'monto':self.monto,
            'cbu':self.cbu,
            'tipo':self.tipo,
            'metodo':'tarjeta',
            'id':0,
        }
class TranferenciaBancaria(models.Model):
    cbu=models.IntegerField()
    monto=models.FloatField()
    nroOperacion=models.IntegerField()
    Cobranza=models.ForeignKey(Cobranza,on_delete=models.CASCADE)
    def to_json(self):
        return{
            'cbu':self.cbu,
            'monto':self.monto,
            'nroOperacion':self.nroOperacion,
            'metodo':'transferencia',
            'id':0,
        }

class VentaCobranza(models.Model):
    monto=models.FloatField()
    Cobranza=models.ForeignKey(Cobranza,on_delete=models.CASCADE)
    Venta=models.ForeignKey(Venta,on_delete=models.CASCADE)
    def to_json(self):
        return {
            'pkVenta':self.Venta.pk,
            'venta':self.Venta.__str__(),
            'monto':self.Venta.get_importeTotal()-self.Venta.get_importeCancelado(),
            'condicion': self.Venta.get_CondicionDePago().__str__(),
            'id':0
        }
    def clean(self):
        if self.monto is not None and self.monto<=0:
            raise ValidationError('no')