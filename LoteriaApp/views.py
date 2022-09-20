from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView
from django.urls import reverse_lazy
from django.core import serializers
import random
from django.utils import timezone
from decimal import Decimal



from LoteriaApp.forms import form_loteria
from LoteriaApp.models import Loteria , Animalito

# Create your views here.





class eliminar_loteria(DeleteView):
    model =  Loteria
    template_name = 'loteria/eliminar_loteria.html'
    success_url = reverse_lazy('LoteriaUrl:listar_jugadasUrl')

    """
        por que al editar el post a esa altura no se encuentra el object que envio por el url tambien puedo utilizar
        el self.get_object() a la altura del post pero este es otra manera
    """
    def dispatch(self, request , *args , **kwargs):
        self.object = self.get_object()
        return super().dispatch(request , *args , **kwargs)

    def post(self, request , *args , **kwargs):

        data={}
        try:
            """
                a esta altura existe el object por lo que realize en el dispatch 
            """
            self.object.delete()

        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data)





class creacion_loteria(CreateView):
    model =  Loteria
    form_class = form_loteria
    template_name = 'loteria/crear_loteria.html'
    success_url = reverse_lazy('LoteriaUrl:listar_jugadasUrl')


    def get_queryset(self):

        consulta = False
        valor =0
        
        while consulta == False:

            comienza = random.randint(1, 500000)
            consulta = self.model.objects.filter(codigo_jugada=comienza)
          
            if consulta:
                consulta= False
            else:
                valor = comienza
                consulta =True

        return valor    


    def post(self, request , *args , **kwargs):
        data = {}
        try:
            # self.get_form() es lo mismo que decir form = self.form_class(request.POST)
            form = self.get_form()

            if form.is_valid():
                data_guardar = self.model()
                data2 = form.cleaned_data
                data_guardar.hora_jugada = data2['hora_jugada']
                data_guardar.monto_jugada = data2['monto_jugada']
                data_guardar.tipo_loteria_relacion = data2['tipo_loteria_relacion']
                data_guardar.codigo_jugada = self.get_queryset()
                data_guardar.save()
                valor =[]

                for x in data2['relacion_animalito']:
                    valor.append(x)
                data_guardar.relacion_animalito.set(valor)
                
            else:
                data['error'] = form.errors

        except Exception as e:
           
            data['error'] = str(e) 

        return JsonResponse(data)    


    


class editar_loteria(UpdateView):
    model =  Loteria
    form_class = form_loteria
    template_name = 'loteria/editar_loteria.html'
    success_url = reverse_lazy('LoteriaUrl:listar_jugadasUrl')




def probando(request):

    data={'informacion': 'campos que mando como informacion'}
    return render(request, 'loteria/modal_detalle_venta.html' ,  {'data':data})


class detalle_venta(DetailView):
    model = Loteria
    template_name= 'loteria/modal_detalle_venta.html'
    pk_url_kwargs= 'pk'	
    

class listar_jugadas(ListView):
    model =  Loteria
    template_name= 'loteria/listar_loteria.html'


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
        suma =0
        for x in fecha_busqueda:
            suma += x.monto_jugada
        resultado_dolares =Decimal(suma) // Decimal(8.22) 
        dato_redondiado = round(resultado_dolares, 3)
        
        
        return resultado_dolares  

    def get_context_data(self, **kwargs):

        context = super().get_context_data (**kwargs)
        #ganancias del dia en bolivares
        context['ganancias__bolivares']= self.generar_ganancias_bolivares()
        #ganancias del dia en dolares
        context['ganancias__dolares']= self. generar_ganancias_dolares
        return context

