from django.contrib import admin
from cobranzas import models
# Register your models here.
class CobranzaAdmin(admin.ModelAdmin):
    pass
class EfectivoAdmin(admin.ModelAdmin):
    pass
class VentaCobranzaAdmmin(admin.ModelAdmin):
    pass
class TransferenciaBancariaAdmin(admin.ModelAdmin):
    #en teoria el nroOperacion no tendria que poder editar
    pass
class TarjetaAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Cobranza,CobranzaAdmin)
admin.site.register(models.Efectivo,EfectivoAdmin)
admin.site.register(models.VentaCobranza,VentaCobranzaAdmmin)
admin.site.register(models.Tarjeta,TarjetaAdmin)
admin.site.register(models.TranferenciaBancaria,TransferenciaBancariaAdmin)