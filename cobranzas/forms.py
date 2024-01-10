from django import forms
from .models import Efectivo,Tarjeta,TranferenciaBancaria,Cobranza
from ventas.models import Afiliado, Venta
from django.utils.timezone import datetime
class CobranzaForm(forms.ModelForm):
    class Meta:
        model=Cobranza
        fields=['monto']
class FechaCobranzaForm(forms.ModelForm):
    class Meta:
        model=Cobranza
        fields=['fecha']
    fecha=forms.DateField(label='Fecha de Cobro',widget=forms.DateInput(attrs={'type':'date'}))
    def __init__(self,*args,**kwargs):
        super(FechaCobranzaForm,self).__init__(*args,**kwargs)
        if not self.instance.pk:
            self.initial['fecha']=datetime.date(datetime.now())
class EfectivoForm(forms.ModelForm):
    class Meta:
        model=Efectivo
        fields=['monto']