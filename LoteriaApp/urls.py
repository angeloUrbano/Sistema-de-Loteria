from django.urls import path
from LoteriaApp.views import *

ReportePersonasPDF2

urlpatterns = [
    path("probandoo/" , probando , name="probandoo"),
    path('jugadas/' , listar_jugadas.as_view() , name="listar_jugadasUrl"),
    path('crear_jugadas/' , creacion_loteria.as_view() , name="crear_jugadasUrl"),
    path('editar_jugadas/<int:pk>/' , editar_loteria.as_view() , name="editar_jugadasUrl"),
     path('editar_loteria2/<int:pk>/<int:pk2>/' , editar_loteria2.as_view() , name="editar_loteria2Url"),
    path('eliminar_jugadas/<int:pk>/' , eliminar_loteria.as_view() , name="eliminar_jugadasUrl"),
    path('eliminar_jugadas2/<int:pk>/' , eliminar_loteria2.as_view() , name="eliminar_juga2dasUrl"),
    path('detalle_jugadas/<int:pk>/' , detalle_venta.as_view() , name="detalle_jugadasUrl"),
    path('detalle_jugadas2/<int:pk>/' , detalle_venta2.as_view() , name="detalle_jugadas2Url"),
    path('jugadas_diarias/' , lista_resumida_vendas_del_dia.as_view() , name="listar_jugadas_diariasUrl"),
    path('divisa/' , editar_valor_divisa.as_view() , name="divisaUrl"),
    path('reporte/' , reporte.as_view() , name="reporteUrl"),
    path('procesar/' , procesar_venta.as_view() , name="procesarUrl"),
    path('crear_venta/' , crear_venta , name="crear_ventaUrl"),
     path('eliminar_venta_multiple/' , eliminar_venta_multiple , name="eliminar_venta_multipleUrl"),
     path('prueba_impresion/' , prueba_impresion , name="prueba_impresionUrl"),
    
        path('ReportePersona2/' , ReportePersonasPDF2 , name="ReportePersonaUrl2"),
        path("reimprimir/<int:id>" , reimprimir , name="reimprimirUrl"),
    

    

]