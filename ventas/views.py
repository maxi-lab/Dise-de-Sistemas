from django.shortcuts import render,HttpResponse
from .forms import VentaForm,VentaDetalleForm
from .models import VentaDetalle
# Create your views here.
def alta_venta(request):
    if request.method=='GET':
        return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
        })      
    if 'submit_venta' in request.POST:
        try:
            form=VentaForm(request.POST)
            nuevaVenta=form.save(commit=False)
            nuevaVenta.save()
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
        })
        except Exception as e:
            #print(e) 
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':'algo fue mal'
        })
