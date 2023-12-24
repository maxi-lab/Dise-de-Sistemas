from django.db import models
from django.utils.timezone import datetime

# Create your models here.
class Afiliado(models.Model):
    cuit=models.IntegerField()
    fechaAfiliacion=models.DateField()
    nombre=models.CharField(max_length=20)
    def __str__(self):
        return self.nombre



class TipoCondicionDePago(models.TextChoices):
    A_PAGAR='A Pagar','aPagar'
    CONTADO='Contado','contado'

class TipoComprobante(models.TextChoices):
    FACTURA_A='A','facturaA'
    FACTURA_B='B','facturaB'
    FACTURA_C='C','facturaC'
    NOTA_CREDITO='N','notaCredito'

class Articulo(models.Model):
    codigo=models.CharField(max_length=20)
    nombre=models.CharField(max_length=20)
    stock=models.IntegerField()
    def __str__(self):
        return self.nombre

class CondicionDePago(models.Model):
    tipo=models.CharField(max_length=20,
                          choices=TipoCondicionDePago.choices)
    def __str__(self):
        return self.tipo

class CondicionDePagoArticulo(models.Model):
    precio=models.FloatField()
    ArticuloId=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    CondicionDePago=models.ForeignKey(CondicionDePago,on_delete=models.CASCADE)
class Venta (models.Model):
    fechaEmision=models.DateField(default=datetime.date(datetime.now()))
    fechaVencimiento=models.DateField(default=datetime.date(datetime.now()))
    importeCancelado=models.FloatField(default=0)
    importeTotal=models.FloatField(default=0)
    tipo=models.CharField(max_length=1,
                          choices=TipoComprobante.choices)
    Afiliado=models.ForeignKey(Afiliado,on_delete=models.CASCADE)
    CondicionDePago=models.ForeignKey(CondicionDePago,on_delete=models.CASCADE)

class VentaDetalle(models.Model):
    cantidad=models.IntegerField()
    precioArticulo=models.FloatField()
    subtotal=models.FloatField()
    Articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    Venta=models.ForeignKey(Venta,on_delete=models.CASCADE)   
     

    









    
