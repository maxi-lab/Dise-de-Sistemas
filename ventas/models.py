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
    A_PAGAR='A Pagar','A Pagar'
    CONTADO='Contado','Contado'

class TipoComprobante(models.TextChoices):
    FACTURA_A='A','Factura A'
    FACTURA_B='B','Factura B'
    FACTURA_C='C','Factura C'
    NOTA_CREDITO='N','Nota de Credito'

class Articulo(models.Model):
    codigo=models.CharField(max_length=20)
    nombre=models.CharField(max_length=20)
    stock=models.IntegerField()
    def __str__(self):
        return self.nombre
    def to_jason(self):
        return{
            'id':self.id,
            'nombre':self.nombre,
            'codigo':self.codigo,
            'stock':self.stock,
        }


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
    def __str__(self):
        return self.Afiliado.nombre+' del '+str(self.fechaEmision)

    def get_CondicionDePago(self):
        return self.CondicionDePago
    def get_importeTotal(self):
        return self.importeTotal
    def get_Afiliado(self):
        return self.Afiliado
    def get_importeCancelado(self):
        return self.importeCancelado
    
class VentaDetalle(models.Model):
    cantidad=models.IntegerField()
    precioArticulo=models.FloatField()
    subtotal=models.FloatField()
    Articulo=models.ForeignKey(Articulo,on_delete=models.CASCADE)
    Venta=models.ForeignKey(Venta,on_delete=models.CASCADE)   
     

    









    
