from django.db import models
from django.utils.timezone import now

# Create your models here.
class Afiliado(models.Model):
    cuit=models.IntegerField()
    fechaAfiliacion=models.DateField()
    nombre=models.CharField(max_length=20)



class TipoCondicionDePago(models.TextChoices):
    A_PAGAR='P','aPagar'
    CONTADO='C','contado'

class TipoComprobante(models.TextChoices):
    FACTURA_A='A','facturaA'
    FACTURA_B='B','facturaB'
    FACTURA_C='C','facturaC'
    NOTA_CREDITO='N','notaCredito'

class Articulo(models.Model):
    codigo=models.CharField(max_length=20)
    nombre=models.CharField(max_length=20)
    stock=models.IntegerField()

class CondicionDePago(models.Model):
    tipo=models.CharField(max_length=1,
                          choices=TipoCondicionDePago.choices)

class CondicionDePagoArticulo(models.Model):
    precio=models.FloatField()
    ArticuloId=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    CondicionDePagoId=models.ForeignKey(CondicionDePago,on_delete=models.CASCADE)

class VentaDetalle(models.Model):
    cantidad=models.IntegerField()
    precioArticulo=models.FloatField()
    subtotal=models.FloatField()
    ArticuloId=models.ForeignKey(Articulo,on_delete=models.CASCADE)

class Venta (models.Model):
    fechaEmision=models.DateField(default=now())
    fechaVencimiento=models.DateField()
    importeCancelado=models.FloatField(default=0)
    importeTotal=models.FloatField()
    tipo=models.CharField(max_length=1,
                          choices=TipoComprobante.choices)
    AfiliadoId=models.ForeignKey(Afiliado,on_delete=models.CASCADE)
    CondicionDePagoId=models.ForeignKey(CondicionDePago,on_delete=models.CASCADE)
    VentaDetalleId=models.ForeignKey(VentaDetalle,on_delete=models.CASCADE)    









    
