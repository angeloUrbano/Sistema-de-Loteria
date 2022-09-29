from LoteriaApp.models import Loteria , Animalito , monto_divisa
from django.utils import timezone
from decimal import Decimal







class consultas_ganancias_mixins():
    
    model = Loteria
    second_model= monto_divisa

    def generar_ganancias_bolivares(self):

        now = timezone.now()
        fecha_busqueda = self.model.objects.filter(creado=now)
        suma =0
        for x in fecha_busqueda:
            suma += x.monto_jugada
        return suma

    def generar_ganancias_dolares(self):

        now = timezone.now()
        fecha_busqueda = self.model.objects.filter(creado=now)
       


        tasa_divisa = self.second_model.objects.all().last()
        # valor_tasa =0
        # for x in tasa_divisa:
        #   valor_tasa = x.monto_en_dolares
        
        print(tasa_divisa.monto_en_dolares)
        suma =0
        for x in fecha_busqueda:
            suma += x.monto_jugada
        resultado_dolares =Decimal(suma) // Decimal(float(tasa_divisa.monto_en_dolares)) 
        dato_redondiado = round(resultado_dolares, 3)
        return resultado_dolares 