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
                attrs={ "class":"fform-inline", 'type': 'time'}
            ),

            'monto_jugada':  forms.NumberInput(
                attrs = {
                    "class":"fform-inline",
                    "placeholder":"ingresa el monto de la jugada",
                   
                    
                }

            ),




            'relacion_animalito':  forms.CheckboxSelectMultiple(attrs={"class":"form-inline row form-check-input", 'style':'margin-left: 25px;'})
        }




