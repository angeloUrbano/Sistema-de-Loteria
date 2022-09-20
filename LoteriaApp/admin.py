from django.contrib import admin

from LoteriaApp.models import Animalito , Loteria , tipo_de_loteria_jugada

# Register your models here.


admin.site.register(Animalito)
admin.site.register(Loteria)
admin.site.register(tipo_de_loteria_jugada)