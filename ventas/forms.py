from django.forms import ModelForm
from django import forms
from .models import Venta
class VentaForm(ModelForm):
    afiliado=forms.CharField(label='Afiliado',required=True)
    class Meta:
        model=Venta
        
        fields=['CondicionDePago','fechaVencimiento','fechaEmision']