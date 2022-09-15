from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.views.generic import ListView , CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy
from django.core import serializers
import random



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
    return render(request, 'base/index2.html' ,  {'data':data})




class listar_jugadas(ListView):
    model =  Loteria
    template_name= 'loteria/listar_loteria.html'
