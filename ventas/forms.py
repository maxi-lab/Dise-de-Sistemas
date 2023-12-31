from django import forms
from .models import Venta,VentaDetalle, Afiliado, Articulo
from django.utils.timezone import datetime
class VentaForm(forms.ModelForm):
    class Meta:
        model=Venta
        fields=['Afiliado','CondicionDePago','fechaVencimiento','fechaEmision','tipo']
        widgets={
            'fechaVencimiento': forms.DateInput(attrs={'type':'date'}),
            'fechaEmision': forms.DateInput(attrs={'type':'date',
                                                   'readonly':True,}), 
        }
    Afiliado = forms.CharField(widget=forms.TextInput(attrs={'name': 'afiliado'}))
    def clean_Afiliado(self):
        afiliadoNombre=self.cleaned_data.get('Afiliado')
        try:
            afiliado=Afiliado.objects.get(nombre=afiliadoNombre)
            return afiliado
        except Afiliado.DoesNotExist:
            raise forms.ValidationError('e')
        
    def __init__(self,*args,**kwargs):
        super(VentaForm,self).__init__(*args,**kwargs)
        if not self.instance.pk:
            self.initial['fechaEmision']=datetime.date(datetime.now())
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