from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.views.generic import ListView , CreateView
from django.urls import reverse_lazy
from django.core import serializers



from LoteriaApp.forms import form_loteria
from LoteriaApp.models import Loteria , Animalito

# Create your views here.






def probando(request):

    data={'informacion': 'campos que mando como informacion'}
    return render(request, 'base/index2.html' ,  {'data':data})




class listar_jugadas(ListView):
    model =  Loteria
    template_name= 'loteria/listar_loteria.html'




class creacion_loteria(CreateView):
    model =  Loteria
    form_class = form_loteria
    template_name = 'loteria/crear_loteria.html'
    success_url = reverse_lazy('LoteriaUrl:listar_jugadasUrl')


    def post(self, request , *args , **kwargs):

        try:
            # self.get_form() es lo mismo que decir form = self.form_class(request.POST)
            form = self.get_form()

            if form.is_valid():

                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
               # return redirect(self.success_url)
            else:
                
                data = {}
                data['error'] = form.errors
                print(data)
               
                return JsonResponse(data)

        except Exception as e:
            return JsonResponse({"form": ""}, status=400)


    
