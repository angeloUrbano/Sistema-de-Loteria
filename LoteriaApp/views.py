from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView ,TemplateView
from django.urls import reverse_lazy
from django.core import serializers
import random
from django.utils import timezone
from decimal import Decimal
from django.contrib.admin.models import LogEntry
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt




from LoteriaApp.forms import form_loteria , monto_divisas_form
from LoteriaApp.models import Loteria , Animalito , monto_divisa , venta_procesada
from LoteriaApp.mixins import consultas_ganancias_mixins

# Create your views here.


class procesar_venta(ListView):
    model = Loteria
    second_model= venta_procesada
    template_name = 'Loteria/venta_procesada.html'


    def get_queryset(self):
        
        query = self.model.objects.filter(procesado=False)
        return query

        


    def get_context_data(self , **kwargs):

        context = super().get_context_data(**kwargs)

        
        context['object_list'] = self.get_queryset()
        return context




    def post(self , request , *args ,**kwargs):
        
        pass       


@csrf_exempt
def crear_venta(request):

    if request.method== "POST":

        prueba = venta_procesada()
        info =  Loteria.objects.filter(procesado=False)
        valor_factura=[]
        for x in info:
            
            valor_factura.append(x.id)
            x.procesado=True
            x.save()
        prueba.save()    
        prueba.relacion_model_loteria.set(valor_factura)

        #return redirect('LoteriaUrl:listar_jugadasUrl')
        dato={'ok':'ok'}
        return JsonResponse(dato)

    

class reporte(TemplateView):
    template_name = 'Loteria/reporte.html'


    
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





class creacion_loteria( LoginRequiredMixin , CreateView):
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
                data_guardar.monto_jugada = data2['monto_jugada']
                data_guardar.tipo_loteria_relacion = data2['tipo_loteria_relacion']
                data_guardar.codigo_jugada = self.get_queryset()
                data_guardar.save()
                valor_animalito =[]
                valor_hora=[]
            
                for x in data2['hora_relacion']:
                    valor_hora.append(x)
                data_guardar.hora_relacion.set(valor_hora)

                for x in data2['relacion_animalito']:
                    valor_animalito.append(x)
                data_guardar.relacion_animalito.set(valor_animalito)
                
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





class editar_valor_divisa(CreateView):
    model =  monto_divisa
    form_class = monto_divisas_form
    template_name = 'loteria/modal_editar_divisaoteria.html'
    success_url = reverse_lazy('LoteriaUrl:listar_jugadasUrl')




def probando(request):

    data= LogEntry.objects.all()
    return render(request, 'login.html' )


class detalle_venta(DetailView):
    model = Loteria
    template_name= 'loteria/modal_detalle_venta.html'
    pk_url_kwargs= 'pk'	
    

class listar_jugadas(LoginRequiredMixin , ListView , consultas_ganancias_mixins):
    model =  Loteria
    template_name= 'loteria/listar_loteria.html'

    consulta= consultas_ganancias_mixins()

    def get_context_data(self, **kwargs):

        context = super().get_context_data (**kwargs)
        #ganancias del dia en bolivares
     
        context['ganancias__bolivares']= self.consulta.generar_ganancias_bolivares()
        #ganancias del dia en dolares
        context['ganancias__dolares']= self.consulta.generar_ganancias_dolares()
        return context



class lista_resumida_vendas_del_dia(ListView , consultas_ganancias_mixins):

    model = Loteria
    template_name = 'loteria/listar_loteria_ventas_diaria.html'
    consulta= consultas_ganancias_mixins()

    def get_queryset(self):

        now = timezone.now()
        queryset = self.model.objects.filter(creado=now)
        return queryset
       

    def get_context_data(self , **kwargs):

        context = super().get_context_data(**kwargs)
        context['object_list']= self.get_queryset() 
        #ganancias del dia en bolivares
        context['ganancias__bolivares']= self.consulta.generar_ganancias_bolivares()
        #ganancias del dia en dolares
        context['ganancias__dolares']= self.consulta.generar_ganancias_dolares() 

      
        return context






def login_view(request):
	
	
	if request.method== 'POST':
		
		
		username = request.POST['email']
		password = request.POST['password']
	
		User = authenticate( username=username, password = password)
		
		
		if User :
			
			login(request , User)
		   
			
			return redirect('LoteriaUrl:listar_jugadasUrl')
		else:
			return render(request ,  "login.html" , {'error': 'Correo o Contraseña Invalido'})	
	return render(request , "login.html")



@login_required
def logout_view(request):
	logout(request)
	return redirect('login') 
      

