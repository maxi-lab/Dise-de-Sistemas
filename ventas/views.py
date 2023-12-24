from django.shortcuts import render,HttpResponse
from .forms import VentaForm,VentaDetalleForm
from .models import VentaDetalle, Venta
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
        #formVenta=VentaForm(request.POST)
        formularioVentaDetalle=VentaDetalleForm(request.POST)
        
        if formularioVentaDetalle.is_valid():
            #venta=formVenta.save(commit=False)
            #formularioVentaDetalle.Venta=venta
            ventaDetalle=formularioVentaDetalle.save(commit=False)
            ventaDetalle.precioArticulo=1
            ventaDetalle.subtotal=ventaDetalle.cantidad
           # ventaDetalle.Venta=venta
            ventaDetalle.save()
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':'algo fue bien'
        })
        else:
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':formularioVentaDetalle.errors})

