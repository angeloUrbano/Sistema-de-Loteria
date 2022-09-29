from django.urls import path
from LoteriaApp.views import *


crear_venta
urlpatterns = [
    path("probandoo/" , probando , name="probandoo"),
    path('jugadas/' , listar_jugadas.as_view() , name="listar_jugadasUrl"),
    path('crear_jugadas/' , creacion_loteria.as_view() , name="crear_jugadasUrl"),
    path('editar_jugadas/<int:pk>/' , editar_loteria.as_view() , name="editar_jugadasUrl"),
    path('eliminar_jugadas/<int:pk>/' , eliminar_loteria.as_view() , name="eliminar_jugadasUrl"),
    path('detalle_jugadas/<int:pk>/' , detalle_venta.as_view() , name="detalle_jugadasUrl"),
    path('jugadas_diarias/' , lista_resumida_vendas_del_dia.as_view() , name="listar_jugadas_diariasUrl"),
    path('divisa/' , editar_valor_divisa.as_view() , name="divisaUrl"),
    path('reporte/' , reporte.as_view() , name="reporteUrl"),
    path('procesar/' , procesar_venta.as_view() , name="procesarUrl"),
     path('crear_venta/' , crear_venta , name="crear_ventaUrl"),
    

    

]