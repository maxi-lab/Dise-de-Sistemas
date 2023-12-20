
from django import forms
from .models import Venta
from django.utils.timezone import datetime
class VentaForm(forms.ModelForm):
    class Meta:
        model=Venta
        fields=['Afiliado','CondicionDePago','fechaVencimiento','fechaEmision']
        widgets={
            'fechaVencimiento': forms.DateInput(attrs={'type':'date'}),
            'fechaEmision': forms.DateInput(attrs={'type':'date'})
        }
    fechaEmision=forms.DateField(widget=forms.TextInput(attrs={'readonly': True}))
    def __init__(self,*args,**kwargs):
        super(VentaForm,self).__init__(*args,**kwargs)
        if not self.instance.pk:
            self.initial['fechaEmision']=datetime.date(datetime.now())#a arreglar