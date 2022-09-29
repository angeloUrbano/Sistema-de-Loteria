from django.contrib import admin

from LoteriaApp.models import Animalito , Loteria , tipo_de_loteria_jugada , monto_divisa , hora_jugada_model , venta_procesada

# Register your models here.


admin.site.register(Animalito)
admin.site.register(Loteria)
admin.site.register(tipo_de_loteria_jugada)
admin.site.register(monto_divisa)
admin.site.register(hora_jugada_model)
admin.site.register(venta_procesada)