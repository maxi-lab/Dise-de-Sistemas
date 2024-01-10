from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CobranzaForm, FechaCobranzaForm, EfectivoForm
# Create your views here.
def alta_cobranza(request):
    metodosPago=request.session.get('metodosPago',[])
    if request.method=='GET':
        print(metodosPago)
        return render(request,'altaCobranza.html',{
            'formCobranza':CobranzaForm,
            'formCobranzaFecha':FechaCobranzaForm,
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
    return render(request,'tarjeta.html')
def tranferencia(request):
    return render(request,'transferencia.html')
