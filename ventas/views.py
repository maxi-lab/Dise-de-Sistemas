from django.shortcuts import render,HttpResponse

# Create your views here.
def alta_venta(request):
    return render(request,'altaVenta.html')