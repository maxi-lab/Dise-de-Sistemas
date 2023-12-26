from django.shortcuts import render,HttpResponse
from .forms import VentaForm,VentaDetalleForm
from .models import VentaDetalle, Venta, Articulo, CondicionDePago, CondicionDePagoArticulo
from django.db import transaction
# Create your views here.
@transaction.atomic
def alta_venta(request):
    ventaDetalles=request.session.get('ventaDetalles',[])
    if request.method=='GET':
        return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
        }) 
    
    if 'submit_venta' in request.POST:
        form=VentaForm(request.POST)
        nuevaVenta=form.save(commit=False)    
        nuevaVenta.save()
        for i in ventaDetalles:
            artId=i['Articulo']
            print(artId)
            articulo=Articulo.objects.get(pk=artId)
            detalle=VentaDetalle.objects.create(
                Venta=nuevaVenta,
                cantidad=i['cantidad'],
                precioArticulo=i['precioArticulo'],
                subtotal=i['subtotal'],
                Articulo=articulo 
            )
            print('creado')
            detalle.save()
            
        ventaDetalles=[]
        try:
            
            request.session['ventaDetalles']=ventaDetalles
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
                'Articulo':ventaDetalle.Articulo.id,
            })
            request.session['ventaDetalles']=ventaDetalles
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':ventaDetalles
        })
        else:
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':formularioVentaDetalle.errors})

