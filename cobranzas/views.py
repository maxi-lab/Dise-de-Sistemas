from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CobranzaForm, FechaCobranzaForm, EfectivoForm,TransferenciaForm,TrajetaForm,VentaCobranzaForm
# Create your views here.
idCookies= 1
def alta_cobranza(request):
    metodosPago=request.session.get('metodosPago',[])
    ventas=request.session.get('ventas',[])
    if request.method!='POST':
        print(metodosPago)
        return render(request,'altaCobranza.html',{
            'formCobranza':CobranzaForm,
            'formCobranzaFecha':FechaCobranzaForm,
            'metodos':metodosPago,
            'totalCobranza':total_actual(metodosPago),
            'formVC':VentaCobranzaForm,
            'ventas':ventas,
            'totalVentas':total_actual(ventas),

        })
    if 'ventas' in request.POST:
         return venta_cobranza(ventas,request,metodosPago)
    
def venta_cobranza(ventas,request,metodosPago):
    formVC=VentaCobranzaForm(request.POST)
    vc=formVC.save(commit=False)
    ventaCobranza=vc.to_json()
    ventas.append(ventaCobranza)
    request.session['ventas']=ventas
    print(ventas)
    print(total_actual(ventas))
    return render(request,'altaCobranza.html',{
            'formCobranza':CobranzaForm,
            'formCobranzaFecha':FechaCobranzaForm,
            'metodos':metodosPago,
            'formVC':VentaCobranzaForm,
            'totalCobranza':total_actual(metodosPago),
            'ventas':ventas,
            'totalVentas':total_actual(ventas),
        })

def efectivo(request):
    metodosPago=request.session.get('metodosPago',[])
    if request.method=='POST':
        formEfectivo=EfectivoForm(request.POST)
        e=formEfectivo.save(commit=False)
        efectivo=e.to_jason()
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
