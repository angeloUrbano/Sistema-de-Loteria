from django.forms import ModelForm
from django.forms import widgets
from django import forms
from LoteriaApp.models import Animalito , Loteria ,  monto_divisa





class form_loteria(ModelForm):

    class Meta:
        model= Loteria
        fields= ['hora_relacion' , 'monto_jugada' , 'relacion_animalito' , 'tipo_loteria_relacion']


        labels={
			'hora_relacion':' Hora de jugada: ',
            'monto_jugada':' Monto de jugada: ',
            'relacion_animalito': ' Animalito: ',
            'tipo_loteria_relacion': 'Loteria: ',
		}

        widgets =  {
            'hora_relacion': forms.SelectMultiple(attrs={'class':'form-control'}),

            'monto_jugada':  forms.NumberInput(
                attrs = {
                    "class":"form-group ",
                    "placeholder":"ingresa el monto de la jugada",
                    "class":"form-control col-sm-7"
                   
                    
                }

            ),




            'relacion_animalito':  forms.CheckboxSelectMultiple(attrs={"class":"form-inline row form-check-input", 'style':'margin-left: 25px;'}),


            'tipo_loteria_relacion': forms.Select(attrs={"class":"custom-select col-sm-3"})
        }






class monto_divisas_form(ModelForm):

    class Meta:
        model = monto_divisa

        fields=['monto_en_dolares']

        label={
            'monto_en_dolares': 'ingrese monto en dolares'
        }

        widgets={
            'monto_en_dolares': forms.NumberInput(
                attrs = {
                    "class":"form-group ",
                    "placeholder":"ingrese la tasa del dolar",
                    "class":"form-control col-sm-30 col-lg-30"
                   
                    
                }

            )
        }