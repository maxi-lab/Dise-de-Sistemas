from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CobranzaForm, FechaCobranzaForm, EfectivoForm,TransferenciaForm,TrajetaForm
# Create your views here.
def alta_cobranza(request):
    metodosPago=request.session.get('metodosPago',[])
    if request.method=='GET':
        print(metodosPago)
        return render(request,'altaCobranza.html',{
            'formCobranza':CobranzaForm,
            'formCobranzaFecha':FechaCobranzaForm,
            'metodos':metodosPago
        })

def efectivo(request):
    metodosPago=request.session.get('metodosPago',[])
    if request.method=='POST':
        formEfectivo=EfectivoForm(request.POST)
        e=formEfectivo.save(commit=False)
        efectivo=e.to_jason()
        metodosPago.append(efectivo)
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
    metodosPago.append(tarjeta)
    request.session['metodosPago']=metodosPago
    return redirect('alta_cobranza')
    
def tranferencia(request):
    metodosPago=request.session.get('metodosPago',[])   
    if request.method!='POST':
        return render(request,'transferencia.html',{'transf':TransferenciaForm,})
    fromTrans=TransferenciaForm(request.POST)
    tr=fromTrans.save(commit=False)
    transferencia=tr.to_json()
    metodosPago.append(transferencia)
    request.session['metodosPago']=metodosPago
    return redirect('alta_cobranza')