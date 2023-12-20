from django.contrib import admin
from ventas import models as v
# Register your models here.
class VentaAdmin(admin.ModelAdmin):
    readonly_fields=('fechaEmision',)
class VentaDetalleAdmin(admin.ModelAdmin):
    pass
class CondicionDePagoAdmin(admin.ModelAdmin):
    pass
class CondicionDePagoArticuloAdmin(admin.ModelAdmin):
    pass
class AfiliadoAdmin(admin.ModelAdmin):
    pass
class ArticuloAdmin(admin.ModelAdmin):
    pass
admin.site.register(v.Afiliado,AfiliadoAdmin)
admin.site.register(v.Articulo,ArticuloAdmin)
admin.site.register(v.VentaDetalle,VentaDetalleAdmin)
admin.site.register(v.Venta,VentaAdmin)
admin.site.register(v.CondicionDePago,CondicionDePagoAdmin)
admin.site.register(v.CondicionDePagoArticulo,CondicionDePagoArticuloAdmin)
