from django.shortcuts import render,HttpResponse
from .forms import VentaForm,VentaDetalleForm
from .models import VentaDetalle
from django.db import transaction
# Create your views here.
@transaction.atomic
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
        except: 
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':'algo fue mal'
        })
    if 'submit_venta_detalle' in request.POST:
        formDetalle=VentaDetalleForm(request.POST)
        nuevoDetalle=formDetalle.save(commit=False)
        nuevoDetalle.precioArticulo=1
        nuevoDetalle.subtotal=nuevoDetalle.cantidad
        nuevoDetalle.save()
        try:
            pass
        except:
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':'algo fue mal en detalle'})

