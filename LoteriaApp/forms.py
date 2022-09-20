from django.forms import ModelForm
from django.forms import widgets
from django import forms
from LoteriaApp.models import Animalito , Loteria





class form_loteria(ModelForm):

    class Meta:
        model= Loteria
        fields= ['hora_jugada' , 'monto_jugada' , 'relacion_animalito' , 'tipo_loteria_relacion']


        labels={
			'hora_jugada':' Hora de jugada: ',
            'monto_jugada':' Monto de jugada: ',
            'relacion_animalito': ' Animalito: ',
            'tipo_loteria_relacion': 'Loteria: ',
		}

        widgets =  {
            'hora_jugada': forms.TimeInput(
                attrs={ "class":"form-group", 'type': 'time' , "class":"form-control col-sm-5"}
            ),

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




