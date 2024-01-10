from django import forms
from .models import Venta,VentaDetalle, Afiliado, Articulo
from django.utils.timezone import datetime
class VentaForm(forms.ModelForm):
    class Meta:
        model=Venta
        fields=['Afiliado','CondicionDePago','tipo']

    
    Afiliado = forms.CharField(widget=forms.TextInput(attrs={'name': 'afiliado'}))
    def clean_Afiliado(self):
        afiliadoNombre=self.cleaned_data.get('Afiliado')
        try:
            afiliado=Afiliado.objects.get(nombre=afiliadoNombre)
            return afiliado
        except Afiliado.DoesNotExist:
            raise forms.ValidationError('e')
        
   
    
class FechasForm(forms.ModelForm):
    class Meta:
        model=Venta
        fields=['fechaVencimiento','fechaEmision',]
    fechaEmision=forms.DateField(label='Fecha de Emision',widget=forms.DateInput(attrs={'type':'date','name':'emi','id':'emi','class':'em'}))
    fechaVencimiento=forms.DateField(label='Fecha de Vencimiento',widget=forms.DateInput(attrs={'type':'date','id':'venc'}))
    
    def __init__(self,*args,**kwargs):
        super(FechasForm,self).__init__(*args,**kwargs)
        if not self.instance.pk:
            self.initial['fechaEmision']=datetime.date(datetime.now())
    def cleaned_emision(self):
        return self['fechaEmision'].value
class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model=VentaDetalle
        fields=['Articulo','cantidad',]
    Articulo=forms.CharField()
    def clean_Articulo(self):
        articuloNombre=self.cleaned_data.get('Articulo')
        try:
            arti=Articulo.objects.get(nombre=articuloNombre)
            return arti
        except Articulo.DoesNotExist:
            raise forms.ValidationError('e')