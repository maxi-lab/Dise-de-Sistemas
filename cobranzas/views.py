from django.shortcuts import render, redirect
import re
from .forms import CobranzaForm, EfectivoForm,TransferenciaForm,TrajetaForm,VentaCobranzaForm
from .models import Efectivo, Tarjeta, TranferenciaBancaria, VentaCobranza,Venta
# Create your views here.
def alta_cobranza(request):
    metodosPago=request.session.get('metodosPago',[])
    ventas=request.session.get('ventas',[])
    if request.method=='GET':
        return render(request,'altaCobranza.html',{
            'formCobranzaFecha':CobranzaForm,
            'metodos':metodosPago,
            'totalCobranza':total_actual(metodosPago),
            'formVC':VentaCobranzaForm,
            'ventas':ventas,
            'totalVentas':total_actual(ventas),
        })
    if 'ventas' in request.POST:
         return venta_cobranza(ventas,request,metodosPago)
    patronMetodos=re.compile(r'met_(\d+)')
    patronVentas=re.compile(r'ven_(\d+)')
    if patronMetodos.findall(str(request.POST)):
        eliminar(metodosPago,patronMetodos.findall(str(request.POST)))
        request.session['metodosPago']=metodosPago
        return render(request,'altaCobranza.html',{
            'formCobranzaFecha':CobranzaForm,
            'metodos':metodosPago,
            'totalCobranza':total_actual(metodosPago),
            'formVC':VentaCobranzaForm,
            'ventas':ventas,
            'totalVentas':total_actual(ventas),
            'mensaje':'Metodo eliminado',
        })
    if patronVentas.findall(str(request.POST)):
        eliminar(ventas,patronVentas.findall(str(request.POST)))
        request.session['ventas']=ventas
        return render(request,'altaCobranza.html',{
            'formCobranzaFecha':CobranzaForm,
            'metodos':metodosPago,
            'totalCobranza':total_actual(metodosPago),
            'formVC':VentaCobranzaForm,
            'ventas':ventas,
            'totalVentas':total_actual(ventas),
            'mensaje':'Venta elimnada ',
        })
    if 'venta_cobranza' in request.POST:
        formCobranza=CobranzaForm(request.POST)
        if formCobranza.is_valid():
            cobranza=formCobranza.save(commit=False)
            cobranza.__setattr__('monto',total_actual(metodosPago))
            cobranza.save()
            persistir_metodo(metodosPago,cobranza)
            metodosPago=[]
            request.session['metodosPago']=metodosPago
            persistir_ventaCobranza(ventas,cobranza)
            ventas=[]
            request.session['ventas']=ventas
            return render(request,'altaCobranza.html',{
            'formCobranzaFecha':CobranzaForm,
            'metodos':metodosPago,
            'totalCobranza':total_actual(metodosPago),
            'formVC':VentaCobranzaForm,
            'ventas':ventas,
            'totalVentas':total_actual(ventas),
            'mensaje':'Cobranza aagregada',
        })
        else:
            print(formCobranza.errors)
    return render(request,'altaCobranza.html',{
            'formCobranzaFecha':CobranzaForm,
            'metodos':metodosPago,
            'totalCobranza':total_actual(metodosPago),
            'formVC':VentaCobranzaForm,
            'ventas':ventas,
            'totalVentas':total_actual(ventas),
        })
    
def venta_cobranza(ventas,request,metodosPago):
    formVC=VentaCobranzaForm(request.POST)
    if formVC.is_valid():
        vc=formVC.save(commit=False)
        ventaCobranza=vc.to_json()
        colocar_nro(ventas,ventaCobranza)
        ventas.append(ventaCobranza)
        request.session['ventas']=ventas
        

    return render(request,'altaCobranza.html',{
            'formCobranzaFecha':CobranzaForm,
            'metodos':metodosPago,
            'totalCobranza':total_actual(metodosPago),
            'formVC':VentaCobranzaForm,
            'ventas':ventas,
            'totalVentas':total_actual(ventas),
            'mensaje':'Venta aagregada',
        })

def efectivo(request):
    metodosPago=request.session.get('metodosPago',[])
    if request.method=='POST':
        formEfectivo=EfectivoForm(request.POST)
        e=formEfectivo.save(commit=False)
        efectivo=e.to_jason()
        colocar_nro(metodosPago,efectivo)
        agregado_inteligente(metodosPago,efectivo )
        print(metodosPago)
        request.session['metodosPago']=metodosPago
        return redirect('alta_cobranza')   
    return render(request,'efectivo.html',{
         'formEfectivo':EfectivoForm,
    })

def tarjeta(request):
    metodosPago=request.session.get('metodosPago',[])
    if request.method!='POST':        
        return render(request,'tarjeta.html',{
            'tarjetaForm':TrajetaForm,
        })
    formTarjeta=TrajetaForm(request.POST)
    t=formTarjeta.save(commit=False)
    tarjeta=t.to_json()
    colocar_nro(metodosPago,tarjeta)
    agregado_inteligente(metodosPago,tarjeta)
    request.session['metodosPago']=metodosPago
    return redirect('alta_cobranza')
    
def tranferencia(request):
    metodosPago=request.session.get('metodosPago',[])   
    if request.method!='POST':
        return render(request,'transferencia.html',{'transf':TransferenciaForm,})
    fromTrans=TransferenciaForm(request.POST)
    tr=fromTrans.save(commit=False)
    transferencia=tr.to_json()
    colocar_nro(metodosPago,transferencia)
    agregado_inteligente(metodosPago,transferencia)
    request.session['metodosPago']=metodosPago
    return redirect('alta_cobranza')

def agregado_inteligente(metodos,obj):
    for i in metodos:
        if  i['metodo']==obj['metodo'] and obj['metodo']=='efectivo':
            i['monto']=i['monto']+obj['monto']
            return
        if obj['metodo']=='transferencia':
            if i['metodo']==obj['metodo'] and obj['cbu']==i['cbu'] and obj['nroOperacion']==i['nroOperacion']:
                i['monto']=i['monto']+obj['monto']
                return
        if obj['metodo']=='tarjeta':
            if i['metodo']==obj['metodo'] and obj['cbu']==i['cbu'] and obj['tipo']==i['tipo']:
                i['monto']=i['monto']+obj['monto']
                return
    metodos.append(obj)

def total_actual(coleccion):
    t=0
    for i in coleccion: 
        t=i['monto']+t
    return t

def colocar_nro(coleccion,obj):
    obj['id']=len(coleccion)+1

def eliminar (coleccion, id):
    i=0
    while i<len(coleccion):
        if coleccion[i]['id']==int (id[0]):
            coleccion.remove(coleccion[i])
            return
        i=i+1

def persistir_metodo(coleccion,cobranza):
    for i in coleccion:
        if i['metodo']=='efectivo':
            efectivo=Efectivo.objects.create(
                monto=i['monto'],
                Cobranza=cobranza,
            )
            efectivo.save()
        if i['metodo']=='tarjeta':
            tarjeta=Tarjeta.objects.create(
                monto=i['monto'],
                cbu=i['cbu'],
                tipo=i['tipo'],
                Cobranza=cobranza,
            )
            tarjeta.save()
        if i['metodo']=='transferencia':
            trans=TranferenciaBancaria.objects.create(
                cbu=i['cbu'],
                monto=i['monto'],
                nroOperacion=i['nroOperacion'],
                Cobranza=cobranza
            )
            trans.save()

def persistir_ventaCobranza(coleccion,obj):
    fondos=obj.monto
    for i in coleccion:
        venta=Venta.objects.get(pk=i['pkVenta'])
        if fondos>i['monto']:
            ventaCobranza=VentaCobranza.objects.create(
                monto=i['monto'],
                Venta=venta,
                Cobranza=obj,
            )
            fondos=fondos-i['monto']
        else:
            ventaCobranza=VentaCobranza.objects.create(
                monto=fondos,
                Venta=venta,
                Cobranza=obj,
            )
            fondos=0
        ventaCobranza.save() 
        if venta.__getattribute__('importeCancelado')<=venta.__getattribute__('importeTotal'):
            venta.__setattr__('importeCancelado',venta.__getattribute__('importeCancelado')+ventaCobranza.__getattribute__('monto'))
            venta.save()