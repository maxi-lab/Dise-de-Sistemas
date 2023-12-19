from django.db import models
from django.utils.timezone import now

# Create your models here.
class TipoCondicionDePago(models.TextChoices):
    A_PAGAR='P','aPagar'
    CONTADO='C','contado'

class TipoComprobante (models.TextChoices):
    FACTURA_A='A','facturaA'
    FACTURA_B='B','facturaB'
    FACTURA_C='C','facturaC'
    NOTA_CREDITO='N','notaCredito'

class Venta (models.Model):
    fechaEmision=models.DateField(default=now())
    fechaVencimiento=models.DateField()
    importeCancelado=models.FloatField(default=0)
    importeTotal=models.FloatField()
    tipo=models.CharField(max_length=1,
                          choices=TipoComprobante.choices)
    
class VentaDetalle(models.Model):
    cantidad=models.IntegerField()
    precioArticulo=models.FloatField()
    subtotal=models.FloatField()

class Articulo(models.Model):
    codigo=models.CharField()
    nombre=models.CharField()
    stock=models.IntegerField()

class CondicionDePagoArticulo(models.Model):
    precio=models.FloatField()

class CondicionDePago(models.Model):
    tipo=models.CharField(max_length=1,
                          choices=TipoCondicionDePago.choices)

class Afiliado(models.Model):
    cuit=models.IntegerField()
    fechaAfiliacion=models.DateField()
    nombre=models.CharField()



    
