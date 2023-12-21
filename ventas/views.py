from django.shortcuts import render,HttpResponse
from .forms import VentaForm,VentaDetalleForm
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
        except: 
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'error':'algo fue mal'
        })
    if 'submit_venta_detalle'in request.POST:  
        try:
            #print('req')
            #print(request.POST)
            formD=VentaDetalleForm(request.POST)
            nuevoDetalle=formD.save(commit=False)
            #print('obj')
            #print(nuevoDetalle)
            
        except:
            
            return render(request,'altaVenta.html',{
            'formVenta':VentaForm,
            'formVentaDetalle':VentaDetalleForm,
            'errorD':'algo fue mal'
        })
