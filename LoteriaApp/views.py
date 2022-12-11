from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView ,TemplateView
from django.urls import reverse_lazy
from django.core import serializers
import random
from django.utils import timezone
from datetime import date , datetime
from decimal import Decimal
from django.contrib.admin.models import LogEntry
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from escpos.printer import Usb
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import (
        Paragraph, 
        Table, 
        SimpleDocTemplate, 
        Spacer, 
        TableStyle, 
        Paragraph)


from reportlab.lib.styles import getSampleStyleSheet
from LoteriaApp.forms import form_loteria , monto_divisas_form , venta_procesadaform
from LoteriaApp.models import Loteria , Animalito , monto_divisa , venta_procesada
from LoteriaApp.mixins import consultas_ganancias_mixins

# Create your views here.


from django.http import FileResponse
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.lib.units import cm
import time






class eliminar_loteria2( LoginRequiredMixin , DeleteView):
    model =  Loteria
    template_name = 'loteria/eliminar_loteria2.html'
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
    
class eliminar_loteria( LoginRequiredMixin , DeleteView):
    model =  venta_procesada
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

def reimprimir(request ,  id):

        prueba = venta_procesada.objects.filter(id=id)
        guardar = venta_procesada()
        valor_factura=[]
        #guardo los id de las loterias y el monto
        for dato in prueba:
            guardar.monto_final_jugadas=dato.monto_final_jugadas
            
            for x in dato.relacion_model_loteria.all():

                valor_factura.append(x.id)
        #creo el codigo nuevo para la factura
        consulta = False
        valor =0
        
        while consulta == False:

            comienza = random.randint(1, 500000)
            consulta = venta_procesada.objects.filter(codigo_jugada=comienza)
          
            if consulta:
                consulta= False
            else:
                valor = comienza
                consulta =True
                
       
        guardar.codigo_jugada=valor
        today = date.today()
        now = datetime.now() 
        guardar.hora = format(today.day)+ "/" + format(today.month) + "/" + format(today.year) + " " + format(now.hour) + ":" +format(now.minute)
        guardar.save() 
        guardar.relacion_model_loteria.set(valor_factura) 
        
        codigo=0
        hora = ""
        for x in prueba:
            codigo=x.codigo_jugada
            hora = x.hora

        # p = Usb(0x416 , 0x5011)
        # p.text(" Las dateras de tu suerte  \n")
        # p.text("fecha:" +  guardar.hora + " \n " )
        # p.text("cod:"  +  str(valor) + " \n ")
        # p.text("vcto 3 dias de sus expedicion \n " )
        # p.text("_______________\n")
        suma = " "
        
        for x in guardar.relacion_model_loteria.all():
            for w in x.tipo_loteria_relacion.all():
                suma += str(w.nombre_tipo_loteria)
                suma += "-"
            
            for y in x.hora_relacion.all():
                suma += str(y.hora_en_nombre)
                suma += '-'
                suma += "\n"   
            for z in x.relacion_animalito.all():
                suma += str(z.codigo_animalito)
                suma += '/'
        suma += " " + 'Bs: ' + str(x.monto_jugada)  
        suma += "\n"
        suma += "-------------------\n"
            
        # p.text(suma)
        # p.text("___________________\n")
        monto =0
        for da in prueba:
            monto=da.monto_final_jugadas
                 
        # p.text("Total: " + str(monto))
        # p.cut()


        return redirect('LoteriaUrl:listar_jugadasUrl')




@login_required
@csrf_exempt
def crear_venta(request):
    info =  Loteria.objects.filter(procesado=False)
    if request.method== "POST" and len(info)>=1:
        prueba = venta_procesada()
      
        valor_factura=[]
        suma=0.0
        multi =0
        
        
        datos_monto = []
        horas_multi=[]
        suma_milti_horas=0
        suma_milti_loterias=0
        for x in info:
            
            valor_factura.append(x.id)
            x.procesado=True
            for y in x.hora_relacion.all():
                suma_milti_horas+=1


            horas_multi.append((suma_milti_horas))
            
            for y in x.tipo_loteria_relacion.all():
                suma_milti_loterias +=1


          
            
            for z in x.relacion_animalito.all():
                multi+=1
            
            datos_monto.append((x.monto_jugada , multi , suma_milti_horas , suma_milti_loterias))
            suma_milti_horas=0
            suma_milti_loterias=0
            multi =0
            x.save()
        
        

        lista_suma = []
        
        indice =0
        for y in datos_monto:
          

            valor1 = (y[0]* y[1]) * y[2] 
            valor = valor1 * y[3] 
            indice =y
            lista_suma.append(valor)
            valor =0

        for a in lista_suma:
            suma = Decimal(suma) + Decimal(a)

        consulta = False
        valor =0
        
        while consulta == False:

            comienza = random.randint(1, 500000)
            consulta = venta_procesada.objects.filter(codigo_jugada=comienza)
          
            if consulta:
                consulta= False
            else:
                valor = comienza
                consulta =True 
        

        
        prueba.codigo_jugada = valor
        prueba.monto_final_jugadas = suma
        today = date.today()
        now = datetime.now() 
        prueba.hora = format(today.day)+ "/" + format(today.month) + "/" + format(today.year) + " " + format(now.hour) + ":" +format(now.minute)
        prueba.save()    
        prueba.relacion_model_loteria.set(valor_factura)

        """ en esta seccion del sistema codifico mi la impresion de la impresora termica """
        
        p = Usb(0x416 , 0x5011)
        p.text(" Las dateras de tu suerte  \n")
        p.text("fecha:" + prueba.hora + " \n " )
        p.text("cod:"  +  str(valor) + " \n ")
        p.text("vcto 3 dias de sus expedicion \n " )
        p.text("_______________\n")
        suma = " "
        for x in prueba.relacion_model_loteria.all():
            for w in x.tipo_loteria_relacion.all():
                suma += str(w.nombre_tipo_loteria)
                suma += "-"
             
            for y in x.hora_relacion.all():
               suma += str(y.hora_en_nombre)
               suma += '-'
            suma += "\n"   
            for z in x.relacion_animalito.all():
               suma += str(z.codigo_animalito)
               suma += '/'
            suma += " " + 'Bs: ' + str(x.monto_jugada)  
            suma += "\n"
            suma += "-------------------\n"
        p.text(suma)
        p.text("___________________\n")
        p.text("Total: " + str(prueba.monto_final_jugadas))
        p.cut()


        return redirect('LoteriaUrl:listar_jugadasUrl')
        dato={'ok':'ok'}
        
        return JsonResponse(dato)

   
    return redirect('LoteriaUrl:listar_jugadasUrl')



@login_required
def ReportePersonasPDF2(request):

    dato1 = request.GET.get("customCheck1")
    dato2 = request.GET.get("customCheck4")
    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment:filename-reporte-report.pdf' 
    buffer= BytesIO()
    c =  canvas.Canvas(buffer , pagesize=A4)


    detalles = [(persona.codigo_jugada, persona.creado, persona.monto_final_jugadas, persona.pago_realizado) for persona in venta_procesada.objects.filter(creado__range=[dato1, dato2])]
    
    

    suma2 =0
    for x in detalles:
        
      
        suma2 += Decimal(x[2])


       

    c.setLineWidth(.3)
    c.setFont('Helvetica' ,22)
    c.drawString(30 , 750 , 'Las dateras de tu suerte')
    c.setFont('Helvetica' ,12)
    c.drawString(30 , 735 , 'Total: ' + str(suma2))
    c.setFont('Helvetica-Bold', 12)
    now = date.today()
    c.drawString(480 , 750 , str(now))
    c.line(460,747,560,747)

    

    c.drawString(480 , 950 , str(now))
    c.line(460,747,560,747)

    
    # tabla header
    styles = getSampleStyleSheet()
    styleBH = styles['Normal']
    styleBH.alignment = TA_CENTER
    styleBH.fontSize=10

    cod = Paragraph('''cod. ''' , styleBH)
    fecha = Paragraph('''fecha. ''' , styleBH)
    b1= Paragraph('''monto. ''' , styleBH)
    b2= Paragraph('''pagado. ''' , styleBH)
    data = []
    data.append([cod , fecha , b1 , b2 ])

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize= 7
    width , height = A4
    high = 700

  
    for x in detalles:
       
        this_detalles = [x[0], x[1] , x[2] , x[3]]
        data.append(this_detalles)
        high = high - 18


    width , height = A4
    table = Table(data , colWidths = [ 2.5 * cm , 2.5 * cm , 2.5 *cm , 2.5 * cm  , 2.5 * cm , 2.5 * cm ])
    table.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(6,6),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))

    table.wrapOn(c, width, height)
    table.drawOn(c, 150 , high)        
    


 
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte.pdf')
     
    







class procesar_venta( LoginRequiredMixin , ListView):
    model = Loteria
    second_model= venta_procesada
    template_name = 'Loteria/venta_procesada.html'


    def get_queryset(self):
        
        query = self.model.objects.filter(procesado=False)
        return query

    def valor_final_fatura_prueba(self):
        info =  self.get_queryset()

        prueba = venta_procesada()
      
        valor_factura=[]
        suma=0.0
        multi =0
        
        
        datos_monto = []
        horas_multi=[]
        suma_milti_horas=0
        suma_milti_loterias=0
        for x in info:
            
            valor_factura.append(x.id)
            #x.procesado=True
            for y in x.hora_relacion.all():
                suma_milti_horas+=1

            for y in x.tipo_loteria_relacion.all():
                suma_milti_loterias +=1


            horas_multi.append((suma_milti_horas))
            
            for z in x.relacion_animalito.all():
                multi+=1
            
            datos_monto.append((x.monto_jugada , multi , suma_milti_horas , suma_milti_loterias))
            suma_milti_horas=0
            suma_milti_loterias=0
            multi =0
            x.save()
        
        

        lista_suma = []
        
        indice =0
        for y in datos_monto:
          

            valor1 = (y[0]* y[1]) * y[2] 
            valor = valor1 * y[3] 
            indice =y
            lista_suma.append(valor)
            valor =0

        for a in lista_suma:
            suma = Decimal(suma) + Decimal(a)

        return suma    


    def get_context_data(self , **kwargs):

        context = super().get_context_data(**kwargs)
       
        
    
        
        context['object_list'] = self.get_queryset()
        context['prueba'] = self.valor_final_fatura_prueba()
        today = date.today()
        now = datetime.now()
        
        
        
        return context




         

@login_required
@csrf_exempt
def prueba_impresion(request):
    p = Usb(0x416 , 0x5011)
    p.text("  ya lo hice mmgv\n")
    p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
    p.cut()





@login_required
@csrf_exempt
def eliminar_venta_multiple(request):
    info =  Loteria.objects.filter(procesado=False)
    if request.method== "POST" and len(info)>=1:
       
       
        for x in info:
            x.delete()
        #return redirect('LoteriaUrl:listar_jugadasUrl')
        dato={'ok':'ok'}
       
        return JsonResponse(dato)

    

class reporte( LoginRequiredMixin , TemplateView):
    template_name = 'Loteria/reporte.html'






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
                
                #data_guardar.codigo_jugada = self.get_queryset()
                data_guardar.save()
                valor_animalito =[]
                valor_hora=[]
                
                valor_loteria=[]

                for x in data2['tipo_loteria_relacion']:
                    valor_loteria.append(x)
                data_guardar.tipo_loteria_relacion.set(valor_loteria)    

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


    


class editar_loteria( LoginRequiredMixin , UpdateView):
    model =  Loteria
    form_class = form_loteria
    template_name = 'loteria/editar_loteria.html'
    success_url = reverse_lazy('LoteriaUrl:procesarUrl')
    


class editar_loteria2( LoginRequiredMixin , UpdateView):
    model =  Loteria
    second_model = venta_procesada
    form_class = form_loteria
    template_name = 'loteria/editar_loteria2.html'
    success_url = reverse_lazy('LoteriaUrl:listar_jugadasUrl')



    def post(self, request , *args , **kwargs):

        instancia = self.model.objects.get(id=self.kwargs['pk'])
        form = self.form_class(request.POST , instance=instancia)
        if form.is_valid():
        
            form.save()

            #edito el valor de monto final de la factura 
            
            instancia2 = self.second_model.objects.filter(pk=self.kwargs['pk2'])
            
            suma = 0
            datos_monto = []
            multi=0
            suma_milti_horas=0
            loterias_multi=0
            code=0
            for x in instancia2:
                code=x.codigo_jugada 
                for z in x.relacion_model_loteria.all():
                    
                    for y  in z.relacion_animalito.all():
                        multi+=1
                    for w in z.hora_relacion.all():
                        suma_milti_horas+=1  

                    for e in z.tipo_loteria_relacion.all():
                        loterias_multi+=1


                    
                    datos_monto.append((z.monto_jugada , multi , suma_milti_horas , loterias_multi))
                    multi=0
                    suma_milti_horas=0
                    loterias_multi=0
            
            lista_suma = []
            indice =0
            
            for y in datos_monto:
            
                
                valor1 = (y[0]* y[1]) * y[2] 
                valor = valor1 * y[3] 
                indice =y
                lista_suma.append(valor)
                valor =0

            for a in lista_suma:
                suma = Decimal(suma) + Decimal(a) 
            update =self.second_model.objects.filter(codigo_jugada=code).update(monto_final_jugadas=suma)
            
            return redirect(self.success_url)

        
        else:
            return render(request, self.template_name , {'form':form})




class editar_valor_divisa( LoginRequiredMixin , CreateView):
    model =  monto_divisa
    form_class = monto_divisas_form
    template_name = 'loteria/modal_editar_divisaoteria.html'
    success_url = reverse_lazy('LoteriaUrl:listar_jugadasUrl')



@login_required
def probando(request):

    data= LogEntry.objects.all()
    return render(request, 'login.html' )

#esta es la url para editar el tiket
class detalle_venta( LoginRequiredMixin , DetailView):
    model = venta_procesada
    template_name= 'loteria/modal_detalle_venta.html'
    pk_url_kwargs= 'pk'	




class detalle_venta2( LoginRequiredMixin , DetailView):
    model = Loteria
    template_name= 'loteria/modal_detalle_venta2.html'
    pk_url_kwargs= 'pk'





    

class listar_jugadas(LoginRequiredMixin , ListView , consultas_ganancias_mixins):
    model =  venta_procesada
    template_name= 'loteria/listar_loteria.html'

    consulta= consultas_ganancias_mixins()

    def get_context_data(self, **kwargs):

        context = super().get_context_data (**kwargs)
        #ganancias del dia en bolivares
   
        context['object_list']= self.model.objects.order_by('id')
        context['ganancias__bolivares']= self.consulta.generar_ganancias_bolivares()
        #ganancias del dia en dolares
        context['ganancias__dolares']= self.consulta.generar_ganancias_dolares()
        return context



class lista_resumida_vendas_del_dia( LoginRequiredMixin , ListView , consultas_ganancias_mixins):

    model = venta_procesada
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
      

