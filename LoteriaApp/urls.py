from django.urls import path
from LoteriaApp.views import *

detalle_venta
urlpatterns = [
    path("probandoo/" , probando , name="probandoo"),
    path('jugadas/' , listar_jugadas.as_view() , name="listar_jugadasUrl"),
    path('crear_jugadas/' , creacion_loteria.as_view() , name="crear_jugadasUrl"),
    path('editar_jugadas/<int:pk>/' , editar_loteria.as_view() , name="editar_jugadasUrl"),
    path('eliminar_jugadas/<int:pk>/' , eliminar_loteria.as_view() , name="eliminar_jugadasUrl"),
    path('eliminar_jugadas/<int:pk>/' , eliminar_loteria.as_view() , name="eliminar_jugadasUrl"),
    path('detalle_jugadas/<int:pk>/' , detalle_venta.as_view() , name="detalle_jugadasUrl"),
    

    

]