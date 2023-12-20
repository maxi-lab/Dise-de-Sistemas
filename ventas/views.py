from django.shortcuts import render,HttpResponse
from .forms import VentaForm
# Create your views here.
def alta_venta(request):
    return render(request,'altaVenta.html',{
        'formVenta':VentaForm,
    })