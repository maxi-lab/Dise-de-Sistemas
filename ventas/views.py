from django.shortcuts import render
from .forms import VentaForm,VentaDetalleForm
from .models import VentaDetalle, Venta, Articulo, CondicionDePago, CondicionDePagoArticulo
from django.db import transaction
# Create your views here.
@transaction.atomic
def alta_venta(request):
    ventaDetalles=request.session.get('ventaDetalles',[])
    if request.method=='GET':
        ventaDetalles=[]
        request.session['ventaDetalles']=ventaDetalles
        return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
        }) 
    
    if 'submit_venta' in request.POST:
        return venta(request,ventaDetalles)
    if 'submit_venta_detalle' in request.POST:
        return venta_detalle(request,ventaDetalles)

def rec_art(id):
    return Articulo.objects.get(pk=id)

def venta(request,ventaDetalles):
    try:
        form=VentaForm(request.POST)
        nuevaVenta=form.save(commit=False)    
        nuevaVenta.save()
        for i in ventaDetalles:
            art=i['Articulo']
            artId=art['id']
            articulo=rec_art(artId)
            detalle=VentaDetalle.objects.create(
                Venta=nuevaVenta,
                cantidad=i['cantidad'],
                precioArticulo=i['precioArticulo'],
                subtotal=i['subtotal'],
                Articulo=articulo 
            )
            detalle.save()
            nuevaVenta.importeTotal=nuevaVenta.importeTotal+detalle.subtotal
            nuevaVenta.save()   
        ventaDetalles=[]
        request.session['ventaDetalles']=ventaDetalles
        return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            })
    except: 
        return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':'algo fue mal',
            'detalles':ventaDetalles,
        })

def venta_detalle(request,ventaDetalles):
    formularioVentaDetalle=VentaDetalleForm(request.POST)
    if formularioVentaDetalle.is_valid():
        ventaDetalle=formularioVentaDetalle.save(commit=False)
        artId=ventaDetalle.Articulo.id
        condPago=CondicionDePagoArticulo.objects.filter(ArticuloId=artId)
        ventaDetalle.precioArticulo=condPago.get().precio
        ventaDetalle.subtotal=ventaDetalle.cantidad*ventaDetalle.precioArticulo
        ventaDetalles.append({
            'cantidad':ventaDetalle.cantidad,
            'precioArticulo':ventaDetalle.precioArticulo,
            'subtotal':ventaDetalle.subtotal,
            'Articulo':Articulo.to_jason(ventaDetalle.Articulo),
            'nom':ventaDetalle.Articulo.nombre
            })
        total=0
        for i in ventaDetalles:
            total=total+i['subtotal']
        request.session['ventaDetalles']=ventaDetalles
        return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':'Detalle cargado exitosamente',
            'detalles':ventaDetalles,
            'total':total,
        })
    else:
        return render(request,'altaVenta.html',{
        'formVenta':VentaForm,
        'formVentaDetalle':VentaDetalleForm,
        'error':formularioVentaDetalle.errors,
        'detalles':ventaDetalles,
        })