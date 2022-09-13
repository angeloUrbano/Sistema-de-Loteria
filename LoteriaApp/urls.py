from django.urls import path
from LoteriaApp.views import *


urlpatterns = [
    path("prueba/" , probando),
    path('jugadas/' , listar_jugadas.as_view() , name="listar_jugadasUrl"),
    path('crear_jugadas/' , creacion_loteria.as_view() , name="crear_jugadasUrl"),
    

    

]