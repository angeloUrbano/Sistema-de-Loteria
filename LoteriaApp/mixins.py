from LoteriaApp.models import Loteria , Animalito , monto_divisa , venta_procesada
from django.utils import timezone
from decimal import Decimal

from datetime import date





class consultas_ganancias_mixins():
    
    model = venta_procesada
    second_model= monto_divisa

    def generar_ganancias_bolivares(self):

        now = date.today()
       
        fecha_busqueda = self.model.objects.filter(creado=now)
        suma =0
        for x in fecha_busqueda:
            suma += x.monto_final_jugadas
        return suma

    def generar_ganancias_dolares(self):

        now = date.today()
        fecha_busqueda = self.model.objects.filter(creado=now)
       


        tasa_divisa = self.second_model.objects.all().last()
        # valor_tasa =0
        # for x in tasa_divisa:
        #   valor_tasa = x.monto_en_dolares
        
        
        suma =0
        for x in fecha_busqueda:
            suma += x.monto_final_jugadas
        resultado_dolares =Decimal(suma) // Decimal(float(tasa_divisa.monto_en_dolares)) 
        dato_redondiado = round(resultado_dolares, 3)
        return resultado_dolares 