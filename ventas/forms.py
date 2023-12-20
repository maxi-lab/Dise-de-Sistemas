
from django import forms
from .models import Venta
from django.utils.timezone import now
class VentaForm(forms.ModelForm):
    class Meta:
        model=Venta
        fields=['Afiliado','CondicionDePago','fechaVencimiento','fechaEmision']
    fechaEmision=forms.CharField( widget=forms.TextInput(attrs={'readonly': True}))
    def __init__(self,*args,**kwargs):
        super(VentaForm,self).__init__(*args,**kwargs)
        if not self.instance.pk:
            self.initial['fechaEmision']=now()#a arreglar