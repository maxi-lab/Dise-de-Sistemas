from django.shortcuts import render
from .forms import VentaForm,VentaDetalleForm
from .models import VentaDetalle, Articulo, CondicionDePagoArticulo
from django.db import transaction
import re
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
    patron=re.compile(r'det_(\d+)')#patron para buscar en los submits
    if patron.findall(str(request.POST)):
        return eliminar_detalle(request,ventaDetalles,patron.findall(str(request.POST)))

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
            'error':'El afiliado no fue encontrado',
            'detalles':ventaDetalles,
            'total':total_actual(ventaDetalles)
        })

def venta_detalle(request,ventaDetalles): 
    formularioVentaDetalle=VentaDetalleForm(request.POST)
    if formularioVentaDetalle.is_valid():
        ventaDetalle=formularioVentaDetalle.save(commit=False)
        if ventaDetalle.cantidad<=0:
            return render(request,'altaVenta.html',{
        'formVenta':VentaForm,
        'formVentaDetalle':VentaDetalleForm,
        'error':'Cantidad invalida',
        'detalles':ventaDetalles,
        'total':total_actual(ventaDetalles),
        })
        artId=ventaDetalle.Articulo.id
        condPago=CondicionDePagoArticulo.objects.filter(ArticuloId=artId)
        ventaDetalle.precioArticulo=condPago.get().precio
        ventaDetalle.subtotal=ventaDetalle.cantidad*ventaDetalle.precioArticulo
        agregado_inteligente(ventaDetalles,{
            'cantidad':ventaDetalle.cantidad,
            'precioArticulo':ventaDetalle.precioArticulo,
            'subtotal':ventaDetalle.subtotal,
            'Articulo':Articulo.to_jason(ventaDetalle.Articulo),
            'nom':ventaDetalle.Articulo.nombre,
            'n':len(ventaDetalles)+1,
            })
        request.session['ventaDetalles']=ventaDetalles
        return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'aviso':'Detalle cargado exitosamente',
            'detalles':ventaDetalles,
            'total':total_actual(ventaDetalles),
        })
    else:
        return render(request,'altaVenta.html',{
        'formVenta':VentaForm,
        'formVentaDetalle':VentaDetalleForm,
        'error':'El articulo no fue encontrado',
        'detalles':ventaDetalles,
        'total':total_actual(ventaDetalles),
        })

def total_actual(ventaDetalles):
    t=0
    for i in ventaDetalles:
        t=t+i['subtotal']
    return t  

def eliminar_detalle(request,ventaDetalles,nro):
    det=None
    for i in ventaDetalles:
        if i['n']==int(nro[0]):
            det=i#si coincide la guardo
    ventaDetalles.remove(det)
    request.session['ventaDetalles']=ventaDetalles
    request.session['ventaDetalles']=ventaDetalles
    return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'aviso':'Detalle eliminado exitosamente',
            'detalles':ventaDetalles,
            'total':total_actual(ventaDetalles),
    })

def agregado_inteligente(ventaDetalles,detalle):
    for i in ventaDetalles:
        if i['Articulo']==detalle['Articulo']:
            print('son iguales')
            i['cantidad']=i['cantidad']+detalle['cantidad']
            i['subtotal']=i['subtotal']+detalle['subtotal']
            return
    ventaDetalles.append(detalle)
    return