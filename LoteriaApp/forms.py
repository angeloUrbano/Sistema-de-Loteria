from django.forms import ModelForm
from django.forms import widgets
from django import forms
from LoteriaApp.models import Animalito , Loteria





class form_loteria(ModelForm):

    class Meta:
        model= Loteria
        fields= ['hora_jugada' , 'monto_jugada' , 'relacion_animalito']

        widgets =  {
            'hora_jugada': forms.TimeInput(
                attrs={'type': 'time'}
            ),

            'monto_jugada':  forms.NumberInput(
                attrs = {
                    "class":"form-control",
                    "placeholder":"ingresa el monto de la jugada",
                   
                    
                }

            ),




            'relacion_animalito':  forms.CheckboxSelectMultiple()
        }




        